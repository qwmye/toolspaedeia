from django.contrib.auth import get_user_model
from django.db import models


class UserPreferences(models.Model):
    """Model to store user preferences for the Paedeia system."""

    class UserColorTheme(models.TextChoices):
        """Predefined color themes for users to choose from."""

        RED = "red", "Red"
        PINK = "pink", "Pink"
        FUCHSIA = "fuchsia", "Fuchsia"
        PURPLE = "purple", "Purple"
        VIOLET = "violet", "Violet"
        INDIGO = "indigo", "Indigo"
        BLUE = "blue", "Blue"
        AZURE = "", "Azure"
        CYAN = "cyan", "Cyan"
        JADE = "jade", "Jade"
        GREEN = "green", "Green"
        LIME = "lime", "Lime"
        YELLOW = "yellow", "Yellow"
        AMBER = "amber", "Amber"
        PUMPKIN = "pumpkin", "Pumpkin"
        ORANGE = "orange", "Orange"
        SAND = "sand", "Sand"
        GRAY = "gray", "Gray"
        ZINC = "zinc", "Zinc"
        SLATE = "slate", "Slate"

    class UserThemeMode(models.TextChoices):
        """Predefined theme modes for users to choose from."""

        LIGHT = "light", "Light"
        DARK = "dark", "Dark"
        SYSTEM = "", "System"

    user = models.OneToOneField(get_user_model(), related_name="preference", on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    theme_mode = models.CharField(max_length=20, blank=True, default="", choices=UserThemeMode.choices)
    color_theme = models.CharField(
        max_length=20,
        default="pumpkin",
        blank=True,
        choices=UserColorTheme.choices,
    )

    class Meta:
        """Meta class for the UserPreferences model."""

        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"

    def __str__(self) -> str:
        return f"Preferences for {self.user.username}"


class Purchase(models.Model):
    """Model to represent a purchase made by a user."""

    user = models.ForeignKey(get_user_model(), related_name="purchases", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Course", related_name="purchases", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for the Purchase model."""

        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"

    def __str__(self) -> str:
        return f"Purchase of {self.course.name} by {self.user.username} on {self.purchase_date}"
