from users.models import UserSitePreferences


def theme_preferences(request):
    theme_mode = ""
    color_theme = ""

    if request.user.is_authenticated:
        try:
            preferences = UserSitePreferences.objects.get(user=request.user)
            theme_mode = preferences.theme_mode or ""
            color_theme = preferences.color_theme or ""
        except UserSitePreferences.DoesNotExist:
            theme_mode = request.COOKIES.get("theme_mode", "")
            color_theme = request.COOKIES.get("color_theme", "")
    else:
        theme_mode = request.COOKIES.get("theme_mode", "")
        color_theme = request.COOKIES.get("color_theme", "")

    return {
        "theme_mode": theme_mode,
        "color_theme": color_theme,
    }
