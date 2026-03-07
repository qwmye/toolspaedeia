from django.contrib.auth import get_user_model
from django.urls import reverse
from django_webtest import WebTest

from courses.models import Course
from users.models import Purchase
from users.models import UserSettings
from users.models import UserSitePreferences


class UsersIntegrationWebTests(WebTest):
    csrf_checks = False

    def setUp(self):
        """Create some initial users and a course."""
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
        self.course = Course.objects.create(
            name="Purchase Candidate",
            description="Course for purchase flow",
            price=12.50,
            is_draft=False,
            publisher=self.publisher,
        )

    def login_through_form(self):
        """Perform the login action through the login form."""
        self.app.reset()
        login_page = self.app.get(reverse("users:login"))
        login_form = login_page.form
        login_form["username"] = self.student.username
        login_form["password"] = "student-pass"  # noqa: S105
        response = login_form.submit()
        while response.status_code in {301, 302, 303, 307, 308}:
            response = response.follow()
        return response

    @staticmethod
    def get_profile_form(profile_page):
        """Return profile form from profile page."""
        return next(form for form in profile_page.forms.values() if form.fields.get("color_theme"))

    @staticmethod
    def get_settings_form(settings_page):
        """Return settings form from settings page."""
        return next(form for form in settings_page.forms.values() if form.fields.get("receive_notifications"))

    @staticmethod
    def get_purchase_form(browse_page):
        """Return purchase form from browse page."""
        return next(
            form for form in browse_page.forms.values() if form.action.endswith(reverse("users:purchase_course"))
        )

    def test_login_view_form_flow(self):
        """
        Happy path login via the form.

        Actions:
            Open login page, fill in valid credentials, submit.
        Behaviour:
            User is authenticated and redirected to home.
        Expectation:
            Browse page renders with course navigation visible and
            no login link shown.
        """
        browse_page = self.login_through_form()

        self.assertEqual(browse_page.status_code, 200)
        self.assertIn("Courses", browse_page.text)
        self.assertIn("Browse Courses", browse_page.text)
        self.assertIn("My Courses", browse_page.text)
        self.assertNotIn("Login", browse_page.text)

    def test_login_view_invalid_credentials_shows_error(self):
        """
        Wrong password keeps the user on the login page with an error.

        Actions:
            Go to login, enter valid username but wrong password,
            submit.
        Behaviour:
            Login page re-renders with the "didn't match" message.
        Expectation:
            Error text is visible, login form is still there, and
            visiting /profile/ still bounces to login.
        """
        login_page = self.app.get(reverse("users:login"))
        login_form = login_page.form
        login_form["username"] = self.student.username
        login_form["password"] = "wrong-pass"  # noqa: S105
        response = login_form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Your username and password didn't match. Please try again.", response.text)
        self.assertIn("Login", response.text)

        profile_response = self.app.get(reverse("users:profile"), expect_errors=True)
        self.assertEqual(profile_response.status_code, 302)
        self.assertIn(reverse("users:login"), profile_response.location)

    def test_login_view_get_when_authenticated_redirects(self):
        """
        Already logged-in user hitting /login/ gets redirected to home.

        Actions:
            Login normally, then GET the login URL a second time.
        Behaviour:
            Server responds with a redirect chain ending at browse.
        Expectation:
            Final page is 200 and shows course content.
        """
        self.login_through_form()

        response = self.app.get(reverse("users:login"), expect_errors=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, reverse("home"))

        redirected_page = response
        while redirected_page.status_code in {301, 302, 303, 307, 308}:
            redirected_page = redirected_page.follow()

        self.assertEqual(redirected_page.status_code, 200)
        self.assertIn("Courses", redirected_page.text)

    def test_profile_view_get_and_post_flow(self):
        """
        View and update profile preferences end-to-end.

        Actions:
            Login, open /profile/, pick blue+dark, submit.
        Behaviour:
            Form saves and redirects back to the same page.
        Expectation:
            Page shows the preferences heading and the DB row
            reflects the new values.
        """
        self.login_through_form()
        profile_page = self.app.get(reverse("users:profile"))

        self.assertEqual(profile_page.status_code, 200)
        self.assertIn("Site Preferences", profile_page.text)
        self.assertIn(self.student.username, profile_page.text)

        profile_form = self.get_profile_form(profile_page)
        profile_form["color_theme"] = "blue"
        profile_form["theme_mode"] = "dark"
        response = profile_form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Site Preferences", response.text)
        preference = UserSitePreferences.objects.get(user=self.student)
        self.assertEqual(preference.color_theme, "blue")
        self.assertEqual(preference.theme_mode, "dark")

    def test_profile_view_post_invalid_choice_shows_validation_error(self):
        """
        Invalid color_theme value triggers a validation error.

        Actions:
            Login, POST profile with color_theme="not-a-valid-color".
        Behaviour:
            Form re-renders with a "Select a valid choice" error.
        Expectation:
            Error message shown, DB still has the defaults (pumpkin, system).
        """
        self.login_through_form()
        response = self.app.post(
            reverse("users:profile"),
            params={"color_theme": "not-a-valid-color", "theme_mode": "dark"},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Select a valid choice. not-a-valid-color is not one of the available choices.", response.text)

        preference = UserSitePreferences.objects.get(user=self.student)
        self.assertEqual(preference.theme_mode, "")
        self.assertEqual(preference.color_theme, "pumpkin")

    def test_purchase_course_post_flow(self):
        """
        Buying a course from the browse page.

        Actions:
            Login, find the purchase button on browse, submit it.
        Behaviour:
            Redirects back to browse; button changes to "Go to Course".
        Expectation:
            Exactly one Purchase row exists for the student+course.
        """
        browse_page = self.login_through_form()
        self.assertIn("Purchase for", browse_page.text)
        purchase_form = self.get_purchase_form(browse_page)
        post_purchase_page = purchase_form.submit().follow()

        self.assertEqual(post_purchase_page.status_code, 200)
        self.assertIn("Go to Course", post_purchase_page.text)
        self.assertTrue(Purchase.objects.filter(user=self.student, course=self.course).exists())
        self.assertEqual(Purchase.objects.filter(user=self.student, course=self.course).count(), 1)

    def test_purchase_course_post_flow_prevents_duplicate_purchase(self):
        """
        Two opened tabs scenario: submitting the same purchase twice is safe.

        Actions:
            Login, grab the purchase form twice (simulating two tabs),
            submit both.
        Behaviour:
            Second POST is silently ignored (get_or_create).
        Expectation:
            Still only one Purchase row; second response redirects to browse and
            shows "Go to Course".
        """
        browse_page = self.login_through_form()

        first_tab_purchase_form = self.get_purchase_form(browse_page)
        second_tab_purchase_form = self.get_purchase_form(browse_page)

        first_tab_purchase_form.submit().follow()
        second_submit_response = second_tab_purchase_form.submit()

        self.assertEqual(second_submit_response.status_code, 302)
        self.assertIn(reverse("courses:course_browse_list"), second_submit_response.location)

        second_landing_page = second_submit_response.follow()
        self.assertEqual(second_landing_page.status_code, 200)
        self.assertIn("Courses", second_landing_page.text)
        self.assertIn("Go to Course", second_landing_page.text)

        self.assertEqual(Purchase.objects.filter(user=self.student, course=self.course).count(), 1)

    def test_purchase_after_logout_redirects_to_login(self):
        """
        Stale purchase form submitted after logging out.

        Actions:
            Login, grab purchase form, logout, then submit the stale
            form.
        Behaviour:
            Redirects to login with "please login" message.
        Expectation:
            No Purchase row created.
        """
        browse_page = self.login_through_form()
        purchase_form = self.get_purchase_form(browse_page)

        self.app.post(reverse("users:logout")).follow()
        logged_out_purchase_response = purchase_form.submit(expect_errors=True)

        self.assertEqual(logged_out_purchase_response.status_code, 302)
        self.assertIn(reverse("users:login"), logged_out_purchase_response.location)

        login_page = logged_out_purchase_response.follow()
        self.assertEqual(login_page.status_code, 200)
        self.assertIn("Please login to see this page.", login_page.text)

        self.assertFalse(Purchase.objects.filter(user=self.student, course=self.course).exists())

    def test_logout_view_post_flow(self):
        """
        Normal logout flow.

        Actions:
            Login, POST the logout endpoint.
        Behaviour:
            Session is cleared, user lands on the login page.
        Expectation:
            Trying to visit /profile/ afterwards redirects to login.
        """
        self.login_through_form()
        logout_response = self.app.post(reverse("users:logout"), expect_errors=True)

        self.assertEqual(logout_response.status_code, 302)
        self.assertEqual(logout_response.location, reverse("users:login"))

        logged_out_page = logout_response.follow()
        self.assertEqual(logged_out_page.status_code, 200)
        self.assertIn("Login", logged_out_page.text)

        after_logout_profile = self.app.get(reverse("users:profile"), expect_errors=True)
        self.assertEqual(after_logout_profile.status_code, 302)
        self.assertIn(reverse("users:login"), after_logout_profile.location)

    def test_logout_view_post_twice_remains_logged_out(self):
        """
        Double logout (e.g. two stale tabs) doesn't raise an exception.

        Actions:
            Login, POST logout twice in a row.
        Behaviour:
            Both POSTs redirect to login without errors.
        Expectation:
            User stays logged out; /profile/ still requires auth.
        """
        self.login_through_form()

        first_logout_response = self.app.post(reverse("users:logout"), expect_errors=True)
        second_logout_response = self.app.post(reverse("users:logout"), expect_errors=True)

        self.assertEqual(first_logout_response.status_code, 302)
        self.assertEqual(first_logout_response.location, reverse("users:login"))
        self.assertEqual(second_logout_response.status_code, 302)
        self.assertEqual(second_logout_response.location, reverse("users:login"))

        profile_after_second_logout = self.app.get(reverse("users:profile"), expect_errors=True)
        self.assertEqual(profile_after_second_logout.status_code, 302)
        self.assertIn(reverse("users:login"), profile_after_second_logout.location)

    def test_settings_view_get_and_post_flow(self):
        """
        View and update user settings end-to-end.

        Actions:
            Login, open /settings/, uncheck notifications, submit.
        Behaviour:
            Form saves and redirects back to the same page.
        Expectation:
            Page shows the settings heading and the DB row
            reflects the updated value.
        """
        self.login_through_form()
        settings_page = self.app.get(reverse("users:settings"))

        self.assertEqual(settings_page.status_code, 200)
        self.assertIn("User Settings", settings_page.text)
        self.assertIn(self.student.username, settings_page.text)

        settings_form = self.get_settings_form(settings_page)
        settings_form["receive_notifications"].checked = False
        response = settings_form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertIn("User Settings", response.text)
        user_settings = UserSettings.objects.get(user=self.student)
        self.assertFalse(user_settings.receive_notifications)

    def test_settings_view_requires_login(self):
        """
        Unauthenticated access to /settings/ redirects to login.

        Actions:
            GET /settings/ without logging in.
        Behaviour:
            302 to login with ?next= param.
        Expectation:
            Redirect to login page.
        """
        response = self.app.get(reverse("users:settings"), expect_errors=True)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.location)

    def test_settings_nav_link_visible(self):
        """
        The settings link is visible in the users nav.

        Actions:
            Login, open the settings page.
        Behaviour:
            Nav sidebar shows "Settings" link.
        Expectation:
            "Settings" appears alongside "Site preferences".
        """
        self.login_through_form()
        settings_page = self.app.get(reverse("users:settings"))

        self.assertIn("Settings", settings_page.text)
        self.assertIn("Site preferences", settings_page.text)
