from decimal import Decimal

from django.db import models

INCOME_TAX = Decimal("0.1")


class Frequency(models.IntegerChoices):
    """Frequency of interest payments."""

    DAILY = 365, "DAILY"
    MONTHLY = 12, "MONTHLY"
    QUARTERLY = 3, "QUARTERLY"
    YEARLY = 1, "YEARLY"


class SavingsAccount(models.Model):
    """Model for a savings account."""

    name = models.CharField()

    per_annum = models.FloatField()
    frequency = models.IntegerField(choices=Frequency)

    def __str__(self) -> str:
        """Set string representation of the savings account."""
        return self.name

    @property
    def actual_interest_rate(self):
        """Compute the actual interest rate after taxes."""
        return Decimal(self.per_annum) / 100 * INCOME_TAX

    def annual_income(self, initial_deposit: float):
        """Compute the annual income of the savings account for a year."""
        return Decimal(initial_deposit) * (
            (1 + Decimal(self.actual_interest_rate) / self.frequency) ** self.frequency - 1
        )
