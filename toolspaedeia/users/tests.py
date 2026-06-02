from django.contrib.auth import get_user_model
from django.urls import reverse
from django_webtest import WebTest

from courses.models import CourseTag
from users.models import UserSitePreferences


class BaseUserWebTest(WebTest):
    csrf_checks = False

    def setUp(self):
        self.publisher = get_user_model().objects.create_user(
            username="publisher",
            email="publisher@example.com",
            password="publisher-pass",  # noqa: S106
        )
        self.student = get_user_model().objects.create_user(
            username="student",
            email="student@example.com",
            password="student-pass",  # noqa: S106
        )

    def login_through_form(self):
        self.app.reset()
        login_page = self.app.get(reverse("users:login"))
        login_form = login_page.forms[1]
        login_form["username"] = self.student.username
        login_form["password"] = "student-pass"  # noqa: S105
        response = login_form.submit()
        while response.status_code in {301, 302, 303, 307, 308}:
            response = response.follow()
        return self.app.get(reverse("courses:course_browse_list"))

    @staticmethod
    def get_preferences_form(preferences_page):
        return next(form for form in preferences_page.forms.values() if form.fields.get("color_theme"))

    @staticmethod
    def get_account_form(account_page):
        return next(form for form in account_page.forms.values() if form.fields.get("username"))


class LoginViewTests(BaseUserWebTest):
    def test_login_view_form_flow(self):
        browse_page = self.login_through_form()

        self.assertEqual(browse_page.status_code, 200)
        self.assertIn("Browse Courses", browse_page.text)
        self.assertNotIn("Login", browse_page.text)

    def test_login_view_invalid_credentials_shows_error(self):
        login_page = self.app.get(reverse("users:login"))
        login_form = login_page.forms[1]
        login_form["username"] = self.student.username
        login_form["password"] = "wrong-pass"  # noqa: S105
        response = login_form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Your username and password didn't match. Please try again.", response.text)
        self.assertIn("Login", response.text)

        preferences_response = self.app.get(reverse("users:preferences"), expect_errors=True)
        self.assertEqual(preferences_response.status_code, 302)
        self.assertIn(reverse("users:login"), preferences_response.location)

    def test_login_view_get_when_authenticated_redirects(self):
        self.login_through_form()

        response = self.app.get(reverse("users:login"), expect_errors=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, reverse("home"))

        redirected_page = response
        while redirected_page.status_code in {301, 302, 303, 307, 308}:
            redirected_page = redirected_page.follow()

        self.assertEqual(redirected_page.status_code, 200)
        self.assertIn("Courses", redirected_page.text)


class LogoutViewTests(BaseUserWebTest):
    def test_logout_view_post_flow(self):
        self.login_through_form()
        logout_response = self.app.post(reverse("users:logout"), expect_errors=True)

        self.assertEqual(logout_response.status_code, 302)
        self.assertEqual(logout_response.location, reverse("users:login"))

        logged_out_page = logout_response.follow()
        self.assertEqual(logged_out_page.status_code, 200)
        self.assertIn("Login", logged_out_page.text)

        after_logout_preferences = self.app.get(reverse("users:preferences"), expect_errors=True)
        self.assertEqual(after_logout_preferences.status_code, 302)
        self.assertIn(reverse("users:login"), after_logout_preferences.location)

    def test_logout_view_post_twice_remains_logged_out(self):
        self.login_through_form()

        first_logout_response = self.app.post(reverse("users:logout"), expect_errors=True)
        second_logout_response = self.app.post(reverse("users:logout"), expect_errors=True)

        self.assertEqual(first_logout_response.status_code, 302)
        self.assertEqual(first_logout_response.location, reverse("users:login"))
        self.assertEqual(second_logout_response.status_code, 302)
        self.assertEqual(second_logout_response.location, reverse("users:login"))

        preferences_after_second_logout = self.app.get(reverse("users:preferences"), expect_errors=True)
        self.assertEqual(preferences_after_second_logout.status_code, 302)
        self.assertIn(reverse("users:login"), preferences_after_second_logout.location)


class UserPreferencesViewTests(BaseUserWebTest):
    def test_preferences_view_get_and_post_flow(self):
        self.login_through_form()
        preferences_page = self.app.get(reverse("users:preferences"))

        self.assertEqual(preferences_page.status_code, 200)
        self.assertIn("Site Preferences", preferences_page.text)
        self.assertIn(self.student.username, preferences_page.text)

        preferences_form = self.get_preferences_form(preferences_page)
        preferences_form["color_theme"] = "blue"
        preferences_form["theme_mode"] = "dark"
        response = preferences_form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Site Preferences", response.text)
        preference = UserSitePreferences.objects.get(user=self.student)
        self.assertEqual(preference.color_theme, "blue")
        self.assertEqual(preference.theme_mode, "dark")

    def test_preferences_view_post_invalid_choice_shows_validation_error(self):
        self.login_through_form()
        response = self.app.post(
            reverse("users:preferences"),
            params={"color_theme": "not-a-valid-color", "theme_mode": "dark"},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Select a valid choice. not-a-valid-color is not one of the available choices.", response.text)

        preference = UserSitePreferences.objects.get(user=self.student)
        self.assertEqual(preference.theme_mode, "")
        self.assertEqual(preference.color_theme, "pumpkin")

    def test_settings_view_get_and_post_flow(self):
        self.login_through_form()
        settings_page = self.app.get(reverse("users:preferences"))

        self.assertEqual(settings_page.status_code, 200)
        self.assertIn("User Site Preferences", settings_page.text)
        self.assertIn(self.student.username, settings_page.text)

        settings_form = next(form for form in settings_page.forms.values() if form.fields.get("receive_notifications"))
        settings_form["receive_notifications"].checked = False
        response = settings_form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertIn("User Site Preferences", response.text)
        user_preferences = UserSitePreferences.objects.get(user=self.student)
        self.assertFalse(user_preferences.receive_notifications)

    def test_settings_view_requires_login(self):
        response = self.app.get(reverse("users:preferences"), expect_errors=True)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.location)

    def test_settings_nav_link_visible(self):
        self.login_through_form()
        settings_page = self.app.get(reverse("users:preferences"))

        self.assertIn("Preferences", settings_page.text)


class UserAccountViewTests(BaseUserWebTest):
    def test_account_view_get_and_post_flow(self):
        self.login_through_form()
        account_page = self.app.get(reverse("users:account"))

        self.assertEqual(account_page.status_code, 200)
        self.assertIn("Account", account_page.text)
        self.assertIn(self.student.username, account_page.text)

        account_form = self.get_account_form(account_page)
        account_form["username"] = "new_student"
        account_form["email"] = "new_student@example.com"
        response = account_form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Account", response.text)
        self.student.refresh_from_db()
        self.assertEqual(self.student.username, "new_student")
        self.assertEqual(self.student.email, "new_student@example.com")

    def test_account_view_password_change_flow(self):
        self.login_through_form()
        account_page = self.app.get(reverse("users:account"))
        account_form = self.get_account_form(account_page)
        account_form["new_password"] = "S3cur3Pa$$w0rd!"  # noqa: S105
        account_form["confirm_password"] = "S3cur3Pa$$w0rd!"  # noqa: S105
        response = account_form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Account", response.text)
        self.student.refresh_from_db()
        self.assertTrue(self.student.check_password("S3cur3Pa$$w0rd!"))

    def test_account_view_mismatched_passwords_shows_error(self):
        self.login_through_form()
        account_page = self.app.get(reverse("users:account"))
        account_form = self.get_account_form(account_page)
        account_form["new_password"] = "Str0ng!P@ss1"  # noqa: S105
        account_form["confirm_password"] = "Str0ng!P@ss2"  # noqa: S105
        response = account_form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Passwords do not match", response.text)

    def test_account_view_requires_login(self):
        response = self.app.get(reverse("users:account"), expect_errors=True)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.location)

    def test_account_nav_link_visible(self):
        self.login_through_form()
        account_page = self.app.get(reverse("users:account"))

        self.assertIn("Account", account_page.text)
        self.assertIn("Preferences", account_page.text)
        self.assertIn("Settings", account_page.text)


class ToggleTagPreferenceViewTests(BaseUserWebTest):
    def test_toggle_tag_preference_view_requires_login(self):
        tag = CourseTag.objects.create(name="Python")
        response = self.app.post(
            reverse("users:toggle_tag_preference"),
            params={"tag_id": tag.id},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.location)

    def test_toggle_tag_preference_view_add_tag(self):
        self.login_through_form()
        tag = CourseTag.objects.create(name="Python")
        preferences, _ = UserSitePreferences.objects.get_or_create(user=self.student)

        self.assertFalse(preferences.preferred_tags.filter(id=tag.id).exists())

        response = self.app.post(
            reverse("users:toggle_tag_preference"),
            params={"tag_id": tag.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("✓ Python", response.text)
        preferences.refresh_from_db()
        self.assertTrue(preferences.preferred_tags.filter(id=tag.id).exists())

    def test_toggle_tag_preference_view_remove_tag(self):
        self.login_through_form()
        tag = CourseTag.objects.create(name="JavaScript")
        preferences, _ = UserSitePreferences.objects.get_or_create(user=self.student)
        preferences.preferred_tags.add(tag)

        self.assertTrue(preferences.preferred_tags.filter(id=tag.id).exists())

        response = self.app.post(
            reverse("users:toggle_tag_preference"),
            params={"tag_id": tag.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("+ JavaScript", response.text)
        preferences.refresh_from_db()
        self.assertFalse(preferences.preferred_tags.filter(id=tag.id).exists())

    def test_toggle_tag_preference_view_missing_tag_id_returns_400(self):
        self.login_through_form()
        response = self.app.post(
            reverse("users:toggle_tag_preference"),
            params={},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing tag_id", response.text)

    def test_toggle_tag_preference_view_nonexistent_tag_returns_404(self):
        self.login_through_form()
        response = self.app.post(
            reverse("users:toggle_tag_preference"),
            params={"tag_id": 99999},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 404)

    def test_toggle_tag_preference_view_preserves_search_query(self):
        self.login_through_form()
        tag = CourseTag.objects.create(name="Python")
        CourseTag.objects.create(name="JavaScript")

        response = self.app.post(
            reverse("users:toggle_tag_preference"),
            params={"tag_id": tag.id, "q": "python"},
            extra_environ={"QUERY_STRING": "q=python"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Python", response.text)
        preferences = UserSitePreferences.objects.get(user=self.student)
        self.assertTrue(preferences.preferred_tags.filter(id=tag.id).exists())

    def test_toggle_tag_preference_view_returns_both_columns(self):
        self.login_through_form()
        tag1 = CourseTag.objects.create(name="Python")
        tag2 = CourseTag.objects.create(name="JavaScript")
        tag3 = CourseTag.objects.create(name="Django")
        preferences, _ = UserSitePreferences.objects.get_or_create(user=self.student)
        preferences.preferred_tags.add(tag1, tag2)

        response = self.app.post(
            reverse("users:toggle_tag_preference"),
            params={"tag_id": tag3.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Available Tags", response.text)
        self.assertIn("Preferred Tags", response.text)
        self.assertIn("✓ Python", response.text)
        self.assertIn("✓ JavaScript", response.text)
        self.assertIn("✓ Django", response.text)
