from django.contrib import admin

from .models import Purchase
from .models import UserSettings
from .models import UserSitePreferences


@admin.register(UserSitePreferences)
class UserSitePreferencesAdmin(admin.ModelAdmin):
    filter_horizontal = ["preferred_tags"]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "course", "amount", "state", "stripe_checkout_session_id", "purchase_date"]
    list_filter = ["state", "purchase_date"]
    search_fields = ["user__username", "course__name", "stripe_checkout_session_id"]


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    pass
