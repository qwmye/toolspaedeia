from django.contrib import admin

from .models import Purchase
from .models import UserSitePreferences


@admin.register(UserSitePreferences)
class UserSitePreferencesAdmin(admin.ModelAdmin):
    pass


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass
