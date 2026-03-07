from django.contrib.auth import get_user_model
from django.db import models


class UserSitePreferences(models.Model):
    """Model to store user preferences for the Paedeia system."""

    class ColorTheme(models.TextChoices):
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

    class ThemeMode(models.TextChoices):
        LIGHT = "light", "Light"
        DARK = "dark", "Dark"
        SYSTEM = "", "System"

    user = models.OneToOneField(get_user_model(), related_name="preferences", on_delete=models.CASCADE)
    theme_mode = models.CharField(max_length=20, blank=True, default="", choices=ThemeMode.choices)
    color_theme = models.CharField(max_length=20, default="pumpkin", blank=True, choices=ColorTheme.choices)

    class Meta:
        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"

    def __str__(self) -> str:
        return f"Preferences for {self.user.username}"


class UserSettings(models.Model):
    """Model to store user settings for the Paedeia system."""

    user = models.OneToOneField(get_user_model(), related_name="settings", on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    receive_notifications = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Settings"
        verbose_name_plural = "User Settings"

    def __str__(self) -> str:
        return f"Settings for {self.user.username}"


class Purchase(models.Model):
    """Model to represent a purchase made by a user."""

    user = models.ForeignKey(get_user_model(), related_name="purchases", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Course", related_name="purchases", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="users_purchase_unique_user_course"),
        ]
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"

    def __str__(self) -> str:
        return f"Purchase of {self.course.name} by {self.user.username} on {self.purchase_date}"
