import contextlib

import stripe
from django.contrib.auth import get_user_model
from django.db import models


class Purchase(models.Model):
    class State(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REFUSED = "REFUSED", "Refused"

    user = models.ForeignKey(get_user_model(), null=True, related_name="purchases", on_delete=models.SET_NULL)
    course = models.ForeignKey("courses.Course", null=True, related_name="purchases", on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    state = models.CharField(max_length=20, choices=State.choices, default=State.ACCEPTED)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users_purchase"
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="users_purchase_unique_user_course"),
        ]
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"

    def __str__(self) -> str:
        return f"{self.state} purchase of {self.course.name} by {self.user.username} on {self.purchase_date}"

    def delete(self, *args, **kwargs):
        if self.state == self.State.ACCEPTED and self.stripe_payment_id:
            with contextlib.suppress(stripe.InvalidRequestError):
                stripe.Refund.create(payment_intent=self.stripe_payment_id)
        return super().delete(*args, **kwargs)
