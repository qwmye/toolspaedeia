from django.utils.deprecation import MiddlewareMixin

from users.models import UserSitePreferences


class ThemeCookieMiddleware(MiddlewareMixin):
    THEME_COOKIE_MAX_AGE = 365 * 24 * 60 * 60  # 1 year

    def process_response(self, request, response):
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
