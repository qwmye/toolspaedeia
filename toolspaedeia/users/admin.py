from django.contrib import admin

from .models import Purchase
from .models import UserSettings
from .models import UserSitePreferences


@admin.register(UserSitePreferences)
class UserSitePreferencesAdmin(admin.ModelAdmin):
    pass


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    pass
