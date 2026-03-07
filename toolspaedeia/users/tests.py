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
        """Create a user for testing preferences view and form submission."""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        self.url = reverse("users:preferences")

    def test_get_requires_authenticated_user(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_get_shows_preferences_form_for_authenticated_user(self):
        """Authenticated users are shown the preferences form."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("User Site Preferences", response.content.decode())

    def test_post_requires_authenticated_user(self):
        """
        Unauthenticated users are redirected when submitting the
        preferences form.
        """
        response = self.client.post(self.url, data={"color_theme": "blue", "theme_mode": "light"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_post_updates_user_preferences(self):
        """Posting valid preferences updates UserSitePreferences record."""
        self.client.force_login(self.user)
        data = {"color_theme": "blue", "theme_mode": "light"}

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)
        pref = UserSitePreferences.objects.get(user=self.user)
        self.assertEqual(pref.color_theme, "blue")
        self.assertEqual(pref.theme_mode, "light")

    def test_post_redirects_to_preferences_on_success(self):
        """Successful POST redirects back to preferences page."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={"color_theme": "green", "theme_mode": "dark"}, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:preferences"))


class TestUserSettingsView(TestCase):
    """Tests for user settings (profile picture, notifications)."""

    def setUp(self):
        """Create a user for testing settings view."""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        self.url = reverse("users:settings")

    def test_get_requires_authenticated_user(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_get_shows_settings_form_for_authenticated_user(self):
        """Authenticated users see the settings form."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("User Settings", response.content.decode())

    def test_get_creates_settings_if_missing(self):
        """Visiting settings creates the UserSettings row via get_or_create."""
        self.client.force_login(self.user)
        self.assertFalse(UserSettings.objects.filter(user=self.user).exists())

        self.client.get(self.url)

        self.assertTrue(UserSettings.objects.filter(user=self.user).exists())

    def test_post_requires_authenticated_user(self):
        """Unauthenticated users are redirected when submitting settings."""
        response = self.client.post(self.url, data={"receive_notifications": True})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_post_updates_receive_notifications(self):
        """Posting valid settings updates the UserSettings record."""
        self.client.force_login(self.user)

        response = self.client.post(self.url, data={"receive_notifications": False})

        self.assertEqual(response.status_code, 302)
        settings = UserSettings.objects.get(user=self.user)
        self.assertFalse(settings.receive_notifications)

    def test_post_redirects_to_settings_on_success(self):
        """Successful POST redirects back to settings page."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={"receive_notifications": True}, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:settings"))


class TestUserAccountView(TestCase):
    """Tests for user account view (username, email, password)."""

    def setUp(self):
        """Create a user for testing the account view."""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        self.url = reverse("users:account")

    def test_get_requires_authenticated_user(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_get_shows_account_form_for_authenticated_user(self):
        """Authenticated users see the account form pre-filled."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Account", response.content.decode())

    def test_post_requires_authenticated_user(self):
        """Unauthenticated users are redirected when submitting."""
        response = self.client.post(self.url, data={"username": "new", "email": "new@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_post_updates_username_and_email(self):
        """Posting valid data updates the user's username and email."""
        self.client.force_login(self.user)
        data = {"username": "newname", "email": "new@example.com"}

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newname")
        self.assertEqual(self.user.email, "new@example.com")

    def test_post_updates_first_and_last_name(self):
        """Posting first/last name updates the user model."""
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
        """Posting matching passwords updates the password hash."""
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
        """Mismatched passwords re-render the form with an error."""
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
        """Taking another user's username re-renders the form with an error."""
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
        """Successful POST redirects back to account page."""
        self.client.force_login(self.user)
        data = {"username": self.user.username, "email": self.user.email}
        response = self.client.post(self.url, data=data, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:account"))

    def test_post_keeps_session_after_password_change(self):
        """Changing the password does not log the user out."""
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
    """Tests for course purchase and enrollment workflow."""

    def setUp(self):
        """Create some initial users and courses for purchase tests."""
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
        """Unauthenticated users are redirected to login."""
        response = self.client.post(self.url, data={"course": self.paid_course.id})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_post_creates_purchase_with_course_price(self):
        """
        Purchasing a course creates a Purchase record with price set from
        the course at that time.
        """
        self.client.force_login(self.student)

        response = self.client.post(self.url, data={"course": self.paid_course.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("courses:course_browse_list"))

        purchase = Purchase.objects.get(user=self.student, course=self.paid_course)

        self.assertEqual(purchase.amount, Decimal("29.99"))

    def test_post_free_course_purchase(self):
        """Enrolling in a free course creates a Purchase with amount=0."""
        self.client.force_login(self.student)

        response = self.client.post(self.url, data={"course": self.free_course.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("courses:course_browse_list"))

        purchase = Purchase.objects.get(user=self.student, course=self.free_course)
        self.assertEqual(purchase.amount, 0.00)

    def test_post_allows_multiple_different_courses_per_user(self):
        """A user is able to purchase multiple courses."""
        self.client.force_login(self.student)
        self.client.post(self.url, data={"course": self.paid_course.id})
        self.client.post(self.url, data={"course": self.free_course.id})

        purchases = Purchase.objects.filter(user=self.student)
        self.assertEqual(purchases.count(), 2)

    def test_post_allows_multiple_users_to_purchase_same_course(self):
        """Multiple users are able to purchase the same course."""
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
    """Tests for the theme preferences context processor."""

    def setUp(self):
        """Create request factory and test user."""
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="themeuser",
            email="themeuser@example.com",
            password="themepass",  # noqa: S106
        )

    def test_theme_preferences_authenticated_user_prefers_database_values(self):
        """Authenticated requests use database preferences over cookies."""
        UserSitePreferences.objects.create(user=self.user, theme_mode="dark", color_theme="blue")
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {"theme_mode": "light", "color_theme": "green"}

        context = theme_preferences(request)

        self.assertEqual(context["theme_mode"], "dark")
        self.assertEqual(context["color_theme"], "blue")

    def test_theme_preferences_authenticated_user_without_preferences_falls_back_to_cookies(self):
        """Authenticated users without preferences fall back to cookies."""
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {"theme_mode": "light", "color_theme": "amber"}

        context = theme_preferences(request)

        self.assertEqual(context["theme_mode"], "light")
        self.assertEqual(context["color_theme"], "amber")

    def test_theme_preferences_anonymous_user_uses_cookie_values(self):
        """Anonymous requests use cookie values."""
        request = self.factory.get("/")
        request.user = AnonymousUser()
        request.COOKIES = {"theme_mode": "dark", "color_theme": "violet"}

        context = theme_preferences(request)

        self.assertEqual(context["theme_mode"], "dark")
        self.assertEqual(context["color_theme"], "violet")


class TestThemeCookieMiddleware(TestCase):
    """Tests for ThemeCookieMiddleware cookie synchronization logic."""

    def setUp(self):
        """Create middleware and reusable test user."""
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="middlewareuser",
            email="middlewareuser@example.com",
            password="middlewarepass",  # noqa: S106
        )
        self.middleware = ThemeCookieMiddleware(lambda _: HttpResponse("ok"))

    def test_theme_cookie_middleware_sets_cookies_when_missing(self):
        """Middleware sets both theme cookies if none are present."""
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
        """Middleware updates only cookies whose values differ from database."""
        UserSitePreferences.objects.create(user=self.user, theme_mode="dark", color_theme="pumpkin")
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {"theme_mode": "light", "color_theme": "pumpkin"}

        response = self.middleware(request)

        self.assertIn("theme_mode", response.cookies)
        self.assertEqual(response.cookies["theme_mode"].value, "dark")
        self.assertNotIn("color_theme", response.cookies)

    def test_theme_cookie_middleware_does_not_set_cookies_when_values_match(self):
        """Middleware skips cookie writes when values already match database."""
        UserSitePreferences.objects.create(user=self.user, theme_mode="light", color_theme="green")
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {"theme_mode": "light", "color_theme": "green"}

        response = self.middleware(request)

        self.assertNotIn("theme_mode", response.cookies)
        self.assertNotIn("color_theme", response.cookies)

    def test_theme_cookie_middleware_authenticated_user_without_preferences_sets_no_cookies(self):
        """Middleware does not set cookies if preferences do not exist."""
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {}

        response = self.middleware(request)

        self.assertNotIn("theme_mode", response.cookies)
        self.assertNotIn("color_theme", response.cookies)

    def test_theme_cookie_middleware_anonymous_user_sets_no_cookies(self):
        """Middleware does not attempt preference sync for anonymous users."""
        request = self.factory.get("/")
        request.user = AnonymousUser()
        request.COOKIES = {}

        response = self.middleware(request)

        self.assertNotIn("theme_mode", response.cookies)
        self.assertNotIn("color_theme", response.cookies)
