from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0016_remove_purchase_model_state"),
        ("courses", "0019_coursetag"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="Purchase",
                    fields=[
                        (
                            "id",
                            models.BigAutoField(
                                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                            ),
                        ),
                        ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                        (
                            "stripe_checkout_session_id",
                            models.CharField(blank=True, max_length=255, null=True, unique=True),
                        ),
                        (
                            "state",
                            models.CharField(
                                choices=[("PENDING", "Pending"), ("ACCEPTED", "Accepted"), ("REFUSED", "Refused")],
                                default="ACCEPTED",
                                max_length=20,
                            ),
                        ),
                        ("purchase_date", models.DateTimeField(auto_now_add=True)),
                        (
                            "course",
                            models.ForeignKey(
                                on_delete=models.deletion.CASCADE,
                                related_name="purchases",
                                to="courses.course",
                            ),
                        ),
                        (
                            "user",
                            models.ForeignKey(
                                on_delete=models.deletion.CASCADE,
                                related_name="purchases",
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                    ],
                    options={
                        "verbose_name": "Purchase",
                        "verbose_name_plural": "Purchases",
                        "db_table": "users_purchase",
                        "constraints": [
                            models.UniqueConstraint(
                                fields=("user", "course"),
                                name="users_purchase_unique_user_course",
                            )
                        ],
                    },
                ),
            ],
        ),
    ]
