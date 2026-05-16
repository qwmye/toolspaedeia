from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0015_merge_usersettings_into_usersitepreferences"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name="Purchase"),
            ],
        ),
    ]
