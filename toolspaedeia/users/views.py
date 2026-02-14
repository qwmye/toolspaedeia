from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View

from users.models import UserPreferences


class UserPreferencesView(View):
    """View to display and manage user preferences."""

    def get(self, request):
        """Handle POST requests to update user preferences."""
        if not (request.user.is_authenticated and request.user.is_active):
            return HttpResponse("Unauthorized", status=401)

        color_theme = request.GET.get("color_theme")
        theme_mode = request.GET.get("theme_mode")
        preferences, _ = UserPreferences.objects.get_or_create(user=request.user)
        if color_theme:
            preferences.color_theme = color_theme
        if theme_mode:
            preferences.theme_mode = theme_mode
        preferences.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))
