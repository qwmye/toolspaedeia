from users.models import UserPreferences


def theme_preferences(request):
    """
    Add theme preferences from cookies to template context.

    For authenticated users, falls back to database values.
    For anonymous users, uses cookies or defaults.
    """
    theme_mode = ""
    color_theme = ""

    # Authenticated users: check database first, fallback to cookies
    if request.user.is_authenticated:
        try:
            preferences = UserPreferences.objects.get(user=request.user)
            theme_mode = preferences.theme_mode or ""
            color_theme = preferences.color_theme or ""
        except UserPreferences.DoesNotExist:
            # Fallback to cookies if no preferences exist
            theme_mode = request.COOKIES.get("theme_mode", "")
            color_theme = request.COOKIES.get("color_theme", "")
    else:
        # Anonymous users: use cookies
        theme_mode = request.COOKIES.get("theme_mode", "")
        color_theme = request.COOKIES.get("color_theme", "")

    return {
        "theme_mode": theme_mode,
        "color_theme": color_theme,
    }
