from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_alter_purchase_options_alter_userpreferences_options"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="purchase",
            constraint=models.UniqueConstraint(fields=("user", "course"), name="users_purchase_unique_user_course"),
        ),
    ]
