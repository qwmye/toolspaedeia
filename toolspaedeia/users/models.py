from django.contrib.auth import get_user_model
from django.db import models


class UserPreferences(models.Model):
    """Model to store user preferences for the Paedeia system."""

    class UserColorTheme(models.TextChoices):
        """Predefined color themes for users to choose from."""

        RED = "Red", "red"
        PINK = "Pink", "pink"
        FUCHSIA = "Fuchsia", "fuchsia"
        PURPLE = "Purple", "purple"
        VIOLET = "Violet", "violet"
        INDIGO = "Indigo", "indigo"
        BLUE = "Blue", "blue"
        AZURE = "Azure", ""
        CYAN = "Cyan", "cyan"
        JADE = "Jade", "jade"
        GREEN = "Green", "green"
        LIME = "Lime", "lime"
        YELLOW = "Yellow", "yellow"
        AMBER = "Amber", "amber"
        PUMPKIN = "Pumpkin", "pumpkin"
        ORANGE = "Orange", "orange"
        SAND = "Sand", "sand"
        GRAY = "Gray", "gray"
        ZINC = "Zinc", "zinc"
        SLATE = "Slate", "slate"

    user = models.OneToOneField(get_user_model(), related_name="preference", on_delete=models.CASCADE)
    theme_mode = models.CharField(max_length=20, blank=True)
    color_theme = models.CharField(
        max_length=20,
        default="pumpkin",
        choices=UserColorTheme.choices,
    )

    def __str__(self) -> str:
        return f"Preferences for {self.user.username}"
