"""Tests for user views, theme context processor, and middleware."""

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
from users.models import UserPreferences


class TestUserProfileFormView(TestCase):
    """Tests for user profile preferences (theme, picture)."""

    def setUp(self):
        """Create a user for testing profile view and form submission."""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        self.url = reverse("users:profile")

    def test_get_requires_authenticated_user(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_get_shows_profile_form_for_authenticated_user(self):
        """Authenticated users are shown the profile form."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Toolspaedeia Site Preferences", response.content.decode())

    def test_post_requires_authenticated_user(self):
        """Unauthenticated users are redirected when submitting profile form."""
        response = self.client.post(self.url, data={"color_theme": "blue", "theme_mode": "light"})
        self.assertEqual(response.status_code, 302)

    def test_post_updates_user_preferences(self):
        """Posting valid preferences updates/creates UserPreferences record."""
        self.client.force_login(self.user)
        data = {"color_theme": "blue", "theme_mode": "light"}

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)
        pref = UserPreferences.objects.get(user=self.user)
        self.assertEqual(pref.color_theme, "blue")
        self.assertEqual(pref.theme_mode, "light")

    def test_post_redirects_to_profile_on_success(self):
        """Successful POST redirects back to profile page."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={"color_theme": "green", "theme_mode": "dark"}, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:profile"))


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
        UserPreferences.objects.create(user=self.user, theme_mode="dark", color_theme="blue")
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
        UserPreferences.objects.create(user=self.user, theme_mode="dark", color_theme="pumpkin")
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
        UserPreferences.objects.create(user=self.user, theme_mode="dark", color_theme="pumpkin")
        request = self.factory.get("/")
        request.user = self.user
        request.COOKIES = {"theme_mode": "light", "color_theme": "pumpkin"}

        response = self.middleware(request)

        self.assertIn("theme_mode", response.cookies)
        self.assertEqual(response.cookies["theme_mode"].value, "dark")
        self.assertNotIn("color_theme", response.cookies)

    def test_theme_cookie_middleware_does_not_set_cookies_when_values_match(self):
        """Middleware skips cookie writes when values already match database."""
        UserPreferences.objects.create(user=self.user, theme_mode="light", color_theme="green")
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
