from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse

from courses.models import Course
from users.context_processors import theme_preferences
from users.middleware import ThemeCookieMiddleware
from users.models import Purchase
from users.models import UserSettings
from users.models import UserSitePreferences


class TestUserPreferencesView(TestCase):
    """Tests for user site preferences (theme)."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        self.url = reverse("users:preferences")

    def test_get_requires_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_get_shows_preferences_form_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("User Site Preferences", response.content.decode())

    def test_post_requires_authenticated_user(self):
        response = self.client.post(self.url, data={"color_theme": "blue", "theme_mode": "light"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_post_updates_user_preferences(self):
        self.client.force_login(self.user)
        data = {"color_theme": "blue", "theme_mode": "light"}

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)
        pref = UserSitePreferences.objects.get(user=self.user)
        self.assertEqual(pref.color_theme, "blue")
        self.assertEqual(pref.theme_mode, "light")

    def test_post_redirects_to_preferences_on_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={"color_theme": "green", "theme_mode": "dark"}, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:preferences"))


class TestUserSettingsView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        self.url = reverse("users:settings")

    def test_get_requires_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_get_shows_settings_form_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("User Settings", response.content.decode())

    def test_get_creates_settings_if_missing(self):
        """Visiting the page auto-creates the UserSettings row."""
        self.client.force_login(self.user)
        self.assertFalse(UserSettings.objects.filter(user=self.user).exists())

        self.client.get(self.url)

        self.assertTrue(UserSettings.objects.filter(user=self.user).exists())

    def test_post_requires_authenticated_user(self):
        response = self.client.post(self.url, data={"receive_notifications": True})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_post_updates_receive_notifications(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, data={"receive_notifications": False})

        self.assertEqual(response.status_code, 302)
        settings = UserSettings.objects.get(user=self.user)
        self.assertFalse(settings.receive_notifications)

    def test_post_redirects_to_settings_on_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={"receive_notifications": True}, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:settings"))


class TestUserAccountView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        self.url = reverse("users:account")

    def test_get_requires_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_get_shows_account_form_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Account", response.content.decode())

    def test_post_requires_authenticated_user(self):
        response = self.client.post(self.url, data={"username": "new", "email": "new@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_post_updates_username_and_email(self):
        self.client.force_login(self.user)
        data = {"username": "newname", "email": "new@example.com"}

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newname")
        self.assertEqual(self.user.email, "new@example.com")

    def test_post_updates_first_and_last_name(self):
        self.client.force_login(self.user)
        data = {
            "username": self.user.username,
            "email": self.user.email,
            "first_name": "Jane",
            "last_name": "Doe",
        }

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(self.user.last_name, "Doe")

    def test_post_changes_password_when_provided(self):
        self.client.force_login(self.user)
        data = {
            "username": self.user.username,
            "email": self.user.email,
            "new_password": "S3cur3Pa$$w0rd!",
            "confirm_password": "S3cur3Pa$$w0rd!",
        }

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("S3cur3Pa$$w0rd!"))

    def test_post_mismatched_passwords_shows_error(self):
        self.client.force_login(self.user)
        data = {
            "username": self.user.username,
            "email": self.user.email,
            "new_password": "newpass123",
            "confirm_password": "differentpass",
        }

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Passwords do not match", response.content.decode())

    def test_post_duplicate_username_shows_error(self):
        """Using another user's username should fail validation."""
        get_user_model().objects.create_user(
            username="taken",
            email="taken@example.com",
            password="takenpass",  # noqa: S106
        )
        self.client.force_login(self.user)
        data = {"username": "taken", "email": self.user.email, "first_name": "", "last_name": ""}

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("already exists", response.content.decode())

    def test_post_redirects_to_account_on_success(self):
        self.client.force_login(self.user)
        data = {"username": self.user.username, "email": self.user.email}
        response = self.client.post(self.url, data=data, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:account"))

    def test_post_keeps_session_after_password_change(self):
        """Changing the password must not invalidate the current session."""
        self.client.force_login(self.user)
        data = {
            "username": self.user.username,
            "email": self.user.email,
            "new_password": "S3cur3Pa$$w0rd!",
            "confirm_password": "S3cur3Pa$$w0rd!",
        }

        self.client.post(self.url, data=data)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)


class TestPurchaseCourseView(TestCase):
    def setUp(self):
        self.publisher = get_user_model().objects.create_user(
            username="publisher",
            email="pub@example.com",
            password="pubpass",  # noqa: S106
        )
        self.student = get_user_model().objects.create_user(
            username="student",
            email="student@example.com",
            password="studentpass",  # noqa: S106
        )
        self.paid_course = Course.objects.create(
            name="Paid Course",
            description="A course that costs money",
            price=29.99,
            publisher=self.publisher,
        )
        self.free_course = Course.objects.create(
            name="Free Course",
            description="A free course",
            price=0.00,
            publisher=self.publisher,
        )
        self.url = reverse("users:purchase_course")

    def test_post_requires_authenticated_user(self):
        response = self.client.post(self.url, data={"course": self.paid_course.id})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_post_creates_purchase_with_course_price(self):
        """Price snapshot is taken from the course at purchase time."""
        self.client.force_login(self.student)

        response = self.client.post(self.url, data={"course": self.paid_course.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("courses:course_browse_list"))

        purchase = Purchase.objects.get(user=self.student, course=self.paid_course)

        self.assertEqual(purchase.amount, Decimal("29.99"))

    def test_post_free_course_purchase(self):
        self.client.force_login(self.student)

        response = self.client.post(self.url, data={"course": self.free_course.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("courses:course_browse_list"))

        purchase = Purchase.objects.get(user=self.student, course=self.free_course)
        self.assertEqual(purchase.amount, 0.00)

    def test_post_allows_multiple_different_courses_per_user(self):
        self.client.force_login(self.student)
        self.client.post(self.url, data={"course": self.paid_course.id})
        self.client.post(self.url, data={"course": self.free_course.id})

        purchases = Purchase.objects.filter(user=self.student)
        self.assertEqual(purchases.count(), 2)

    def test_post_allows_multiple_users_to_purchase_same_course(self):
        other_student = get_user_model().objects.create_user(
            username="other",
            email="other@example.com",
            password="pass",  # noqa: S106
        )

        self.client.force_login(self.student)
        self.client.post(self.url, data={"course": self.paid_course.id})

        self.client.force_login(other_student)
        self.client.post(self.url, data={"course": self.paid_course.id})

        purchases = Purchase.objects.filter(course=self.paid_course)
        self.assertEqual(purchases.count(), 2)


class TestThemeContextProcessor(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="themeuser",
            email="themeuser@example.com",
            password="themepass",  # noqa: S106
        )

    def test_theme_preferences_authenticated_user_prefers_database_values(self):
        """DB preferences take priority over cookie values."""
        UserSitePreferences.objects.create(user=self.user, theme_mode="dark", color_theme="blue")
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {"theme_mode": "light", "color_theme": "green"}

        context = theme_preferences(request)

        self.assertEqual(context["theme_mode"], "dark")
        self.assertEqual(context["color_theme"], "blue")

    def test_theme_preferences_authenticated_user_without_preferences_falls_back_to_cookies(self):
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {"theme_mode": "light", "color_theme": "amber"}

        context = theme_preferences(request)

        self.assertEqual(context["theme_mode"], "light")
        self.assertEqual(context["color_theme"], "amber")

    def test_theme_preferences_anonymous_user_uses_cookie_values(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        request.COOKIES = {"theme_mode": "dark", "color_theme": "violet"}

        context = theme_preferences(request)

        self.assertEqual(context["theme_mode"], "dark")
        self.assertEqual(context["color_theme"], "violet")


class TestThemeCookieMiddleware(TestCase):
    """Cookie sync logic: only write cookies when the DB value differs."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="middlewareuser",
            email="middlewareuser@example.com",
            password="middlewarepass",  # noqa: S106
        )
        self.middleware = ThemeCookieMiddleware(lambda _: HttpResponse("ok"))

    def test_theme_cookie_middleware_sets_cookies_when_missing(self):
        UserSitePreferences.objects.create(user=self.user, theme_mode="dark", color_theme="pumpkin")
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {}

        response = self.middleware(request)

        self.assertIn("theme_mode", response.cookies)
        self.assertEqual(response.cookies["theme_mode"].value, "dark")
        self.assertIn("color_theme", response.cookies)
        self.assertEqual(response.cookies["color_theme"].value, "pumpkin")

    def test_theme_cookie_middleware_sets_only_cookie_with_changed_value(self):
        """Only the cookie that differs from the DB row gets rewritten."""
        UserSitePreferences.objects.create(user=self.user, theme_mode="dark", color_theme="pumpkin")
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {"theme_mode": "light", "color_theme": "pumpkin"}

        response = self.middleware(request)

        self.assertIn("theme_mode", response.cookies)
        self.assertEqual(response.cookies["theme_mode"].value, "dark")
        self.assertNotIn("color_theme", response.cookies)

    def test_theme_cookie_middleware_does_not_set_cookies_when_values_match(self):
        UserSitePreferences.objects.create(user=self.user, theme_mode="light", color_theme="green")
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {"theme_mode": "light", "color_theme": "green"}

        response = self.middleware(request)

        self.assertNotIn("theme_mode", response.cookies)
        self.assertNotIn("color_theme", response.cookies)

    def test_theme_cookie_middleware_authenticated_user_without_preferences_sets_no_cookies(self):
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {}

        response = self.middleware(request)

        self.assertNotIn("theme_mode", response.cookies)
        self.assertNotIn("color_theme", response.cookies)

    def test_theme_cookie_middleware_anonymous_user_sets_no_cookies(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        request.COOKIES = {}

        response = self.middleware(request)

        self.assertNotIn("theme_mode", response.cookies)
        self.assertNotIn("color_theme", response.cookies)
