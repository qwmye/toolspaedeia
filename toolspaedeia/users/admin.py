from django.contrib import admin

from .models import UserSitePreferences


@admin.register(UserSitePreferences)
class UserSitePreferencesAdmin(admin.ModelAdmin):
    filter_horizontal = ["preferred_tags"]
