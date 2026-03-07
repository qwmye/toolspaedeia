from django.utils.deprecation import MiddlewareMixin

from users.models import UserSitePreferences


class ThemeCookieMiddleware(MiddlewareMixin):
    """
    Middleware to set theme cookies only when necessary.

    Sets cookies only if:
    - No cookie exists, or
    - Existing cookie differs from user's current preference

    This keeps cookies in sync with database while minimizing cookie updates.
    """

    THEME_COOKIE_MAX_AGE = 365 * 24 * 60 * 60  # 1 year in seconds

    def process_response(self, request, response):
        """Synchronize theme cookies with user preferences when needed."""
        if request.user.is_authenticated:
            try:
                preferences = UserSitePreferences.objects.get(user=request.user)

                current_theme_mode = request.COOKIES.get("theme_mode")
                if current_theme_mode != preferences.theme_mode:
                    response.set_cookie("theme_mode", preferences.theme_mode, max_age=self.THEME_COOKIE_MAX_AGE)

                current_color_theme = request.COOKIES.get("color_theme")
                if current_color_theme != preferences.color_theme:
                    response.set_cookie("color_theme", preferences.color_theme, max_age=self.THEME_COOKIE_MAX_AGE)
            except UserSitePreferences.DoesNotExist:
                pass

        return response
