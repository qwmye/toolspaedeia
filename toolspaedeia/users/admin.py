from django.contrib import admin

from .models import Purchase
from .models import UserPreferences


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    """Admin interface for managing user preferences."""


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """Admin interface for managing user purchases."""
