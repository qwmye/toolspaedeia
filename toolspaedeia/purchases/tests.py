from django.contrib.auth import get_user_model
from django.urls import reverse
from django_webtest import WebTest

from courses.models import Course
from purchases.models import Purchase


class PurchasesIntegrationWebTests(WebTest):
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
        self.course = Course.objects.create(
            name="Purchase Candidate",
            description="Course for purchase flow",
            price=12.50,
            is_draft=False,
            publisher=self.publisher,
        )

    def login_through_form(self):
        """Log the student in via the login form and navigate to browse page."""
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
    def get_purchase_form(browse_page):
        return next(
            form for form in browse_page.forms.values() if form.action.endswith(reverse("purchases:purchase_course"))
        )

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
