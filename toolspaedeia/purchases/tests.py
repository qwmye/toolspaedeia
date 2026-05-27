from django.contrib.auth import get_user_model
from django.urls import reverse
from django_webtest import WebTest

from courses.models import Course
from courses.models import Module
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
        self.module_public = Module.objects.create(
            course=self.course,
            title="Public Module",
            description="Visible module",
            content="Content",
            order=1,
            is_draft=False,
        )
        self.module_draft = Module.objects.create(
            course=self.course,
            title="Draft Module",
            description="Draft module",
            content="Draft",
            order=2,
            is_draft=True,
        )
        self.pending_course = Course.objects.create(
            name="Pending Candidate",
            description="Course with non-accepted purchase",
            price=8.50,
            is_draft=False,
            publisher=self.publisher,
        )
        self.pending_module = Module.objects.create(
            course=self.pending_course,
            title="Pending Module",
            description="Pending module",
            content="Pending",
            order=1,
            is_draft=False,
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
    def get_purchase_form(browse_page):
        return next(
            form for form in browse_page.forms.values() if form.action.endswith(reverse("purchases:purchase_course"))
        )

    def test_purchase_course_post_flow(self):
        browse_page = self.login_through_form()
        self.assertIn("Purchase for", browse_page.text)
        purchase_form = self.get_purchase_form(browse_page)
        post_purchase_page = purchase_form.submit().follow()

        self.assertEqual(post_purchase_page.status_code, 200)
        self.assertIn("Go to Course", post_purchase_page.text)
        self.assertTrue(Purchase.objects.filter(user=self.student, course=self.course).exists())
        self.assertEqual(Purchase.objects.filter(user=self.student, course=self.course).count(), 1)

    def test_purchase_course_post_flow_prevents_duplicate_purchase(self):
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

    def test_offline_map_requires_login(self):
        response = self.app.get(reverse("purchases:offline_map"), expect_errors=True)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.location)

    def test_offline_map_contains_only_accepted_course_pages(self):
        Purchase.objects.create(
            user=self.student,
            course=self.course,
            amount=self.course.price,
            state=Purchase.State.ACCEPTED,
        )
        Purchase.objects.create(
            user=self.student,
            course=self.pending_course,
            amount=self.pending_course.price,
            state=Purchase.State.PENDING,
        )

        self.app.reset()
        self.app.set_user(self.student.username)
        response = self.app.get(reverse("purchases:offline_map"))
        payload = response.json

        expected_course_url = reverse("courses:course_detail", kwargs={"course_id": self.course.id})
        expected_module_url = reverse(
            "courses:module_detail",
            kwargs={"course_id": self.course.id, "module_id": self.module_public.id},
        )
        draft_module_url = reverse(
            "courses:module_detail",
            kwargs={"course_id": self.course.id, "module_id": self.module_draft.id},
        )
        pending_course_url = reverse("courses:course_detail", kwargs={"course_id": self.pending_course.id})

        self.assertEqual(response.status_code, 200)
        self.assertIn("urls", payload)
        self.assertIn(expected_course_url, payload["urls"])
        self.assertIn(expected_module_url, payload["urls"])
        self.assertNotIn(draft_module_url, payload["urls"])
        self.assertNotIn(pending_course_url, payload["urls"])
