from decimal import Decimal

from django.db import models

INCOME_TAX = Decimal(0.1)


class Frequency(models.IntegerChoices):
    DAILY = 365, "DAILY"
    MONTHLY = 12, "MONTHLY"
    QUARTERLY = 3, "QUARTERLY"
    YEARLY = 1, "YEARLY"


class SavingsAccount(models.Model):
    name = models.CharField()

    per_annum = models.FloatField()
    frequency = models.IntegerField(choices=Frequency)

    @property
    def actual_interest_rate(self):
        return Decimal(self.per_annum) / 100 * INCOME_TAX

    def annual_income(self, initial_deposit: float):
        return initial_deposit * ((1 + Decimal(self.actual_interest_rate) / self.frequency) ** self.frequency - 1)
