from unittest.mock import MagicMock
from unittest.mock import patch

import stripe
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
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

    def test_enroll_course_post_flow(self):
        browse_page = self.login_through_form()
        self.assertIn("Purchase for", browse_page.text)

        post_response = self.app.post(
            reverse("purchases:enroll_course"),
            params={"course": str(self.course.id)},
        )
        post_purchase_page = post_response.follow()

        self.assertEqual(post_purchase_page.status_code, 200)
        self.assertIn("Go to Course", post_purchase_page.text)
        self.assertTrue(Purchase.objects.filter(user=self.student, course=self.course).exists())
        self.assertEqual(Purchase.objects.filter(user=self.student, course=self.course).count(), 1)

    def test_enroll_course_post_flow_prevents_duplicate_purchase(self):
        self.login_through_form()

        first_response = self.app.post(
            reverse("purchases:enroll_course"),
            params={"course": str(self.course.id)},
        )
        first_response.follow()

        second_submit_response = self.app.post(
            reverse("purchases:enroll_course"),
            params={"course": str(self.course.id)},
        )

        self.assertEqual(second_submit_response.status_code, 302)
        self.assertIn(reverse("courses:course_browse_list"), second_submit_response.location)

        second_landing_page = second_submit_response.follow()
        self.assertEqual(second_landing_page.status_code, 200)
        self.assertIn("Courses", second_landing_page.text)
        self.assertIn("Go to Course", second_landing_page.text)

        self.assertEqual(Purchase.objects.filter(user=self.student, course=self.course).count(), 1)

    def test_purchase_after_logout_redirects_to_login(self):
        self.login_through_form()

        self.app.post(reverse("users:logout")).follow()
        logged_out_purchase_response = self.app.post(
            reverse("purchases:enroll_course"),
            params={"course": str(self.course.id)},
            expect_errors=True,
        )

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

    def test_offline_map_empty_for_no_purchases(self):
        self.app.reset()
        self.app.set_user(self.student.username)
        response = self.app.get(reverse("purchases:offline_map"))
        payload = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["urls"], [])

    def test_offline_map_multiple_courses_and_modules(self):
        free_course = Course.objects.create(
            name="Free Course",
            description="No payment",
            price=0,
            is_draft=False,
            publisher=self.publisher,
        )
        module1 = Module.objects.create(
            course=free_course,
            title="Module 1",
            description="First",
            content="Content 1",
            order=1,
            is_draft=False,
        )
        module2 = Module.objects.create(
            course=free_course,
            title="Module 2",
            description="Second",
            content="Content 2",
            order=2,
            is_draft=False,
        )

        Purchase.objects.create(
            user=self.student,
            course=self.course,
            amount=self.course.price,
            state=Purchase.State.ACCEPTED,
        )
        Purchase.objects.create(
            user=self.student,
            course=free_course,
            amount=0,
            state=Purchase.State.ACCEPTED,
        )

        self.app.reset()
        self.app.set_user(self.student.username)
        response = self.app.get(reverse("purchases:offline_map"))
        payload = response.json
        urls = payload["urls"]

        course1_url = reverse("courses:course_detail", kwargs={"course_id": self.course.id})
        course2_url = reverse("courses:course_detail", kwargs={"course_id": free_course.id})
        module1_url = reverse(
            "courses:module_detail", kwargs={"course_id": self.course.id, "module_id": self.module_public.id}
        )
        free_module1_url = reverse(
            "courses:module_detail", kwargs={"course_id": free_course.id, "module_id": module1.id}
        )
        free_module2_url = reverse(
            "courses:module_detail", kwargs={"course_id": free_course.id, "module_id": module2.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(course1_url, urls)
        self.assertIn(course2_url, urls)
        self.assertIn(module1_url, urls)
        self.assertIn(free_module1_url, urls)
        self.assertIn(free_module2_url, urls)


class EnrollmentDialogIntegrationTests(WebTest):
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
        self.paid_course = Course.objects.create(
            name="Paid Course",
            description="Premium content",
            price=25.00,
            is_draft=False,
            publisher=self.publisher,
        )
        self.free_course = Course.objects.create(
            name="Free Course",
            description="No payment needed",
            price=0,
            is_draft=False,
            publisher=self.publisher,
        )

    def test_enrollment_dialog_requires_login(self):
        response = self.app.get(
            reverse("purchases:enrollment_dialog"),
            params={"course_id": self.paid_course.id},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.location)

    def test_enrollment_dialog_missing_course_id_returns_400(self):
        self.app.set_user(self.student.username)
        response = self.app.get(
            reverse("purchases:enrollment_dialog"),
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 400)

    def test_enrollment_dialog_nonexistent_course_returns_404(self):
        self.app.set_user(self.student.username)
        response = self.app.get(
            reverse("purchases:enrollment_dialog"),
            params={"course_id": 99999},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 404)

    def test_enrollment_dialog_draft_course_returns_404(self):
        draft_course = Course.objects.create(
            name="Draft Course",
            description="Not published",
            price=10.00,
            is_draft=True,
            publisher=self.publisher,
        )
        self.app.set_user(self.student.username)
        response = self.app.get(
            reverse("purchases:enrollment_dialog"),
            params={"course_id": draft_course.id},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 404)

    def test_enrollment_dialog_already_purchased_returns_400(self):
        Purchase.objects.create(
            user=self.student,
            course=self.paid_course,
            amount=self.paid_course.price,
            state=Purchase.State.ACCEPTED,
        )
        self.app.set_user(self.student.username)
        with patch.object(stripe.PaymentLink, "create") as mock_create:
            mock_create.return_value = MagicMock(url="https://buy.stripe.com/test")
            response = self.app.get(
                reverse("purchases:enrollment_dialog"),
                params={"course_id": self.paid_course.id},
                expect_errors=True,
            )

        self.assertEqual(response.status_code, 400)
        self.assertIn("already purchased", response.text)

    def test_enrollment_dialog_has_open_attribute(self):
        self.app.set_user(self.student.username)
        response = self.app.get(
            reverse("purchases:enrollment_dialog"),
            params={"course_id": self.free_course.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('<dialog id="confirm-', response.text)
        self.assertIn("open", response.text)


class CreateRefundIntegrationTests(WebTest):
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
            name="Refundable Course",
            description="Can be refunded",
            price=15.00,
            is_draft=False,
            publisher=self.publisher,
        )

    def test_refund_requires_login(self):
        response = self.app.post(
            reverse("purchases:create_refund"),
            params={"course_id": self.course.id},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.location)

    def test_refund_missing_course_id_returns_400(self):
        self.app.set_user(self.student.username)
        response = self.app.post(
            reverse("purchases:create_refund"),
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 400)

    def test_refund_deletes_purchase(self):
        purchase = Purchase.objects.create(
            user=self.student,
            course=self.course,
            amount=self.course.price,
            state=Purchase.State.ACCEPTED,
            stripe_payment_id="pi_test123",
        )

        self.app.set_user(self.student.username)
        with patch.object(stripe.Refund, "create") as mock_refund:
            mock_refund.return_value = MagicMock()
            response = self.app.post(
                reverse("purchases:create_refund"),
                params={"course_id": self.course.id},
            )

        self.assertEqual(response.status_code, 201)
        self.assertFalse(Purchase.objects.filter(id=purchase.id).exists())

    def test_refund_redirects_to_purchased_courses(self):
        Purchase.objects.create(
            user=self.student,
            course=self.course,
            amount=self.course.price,
            state=Purchase.State.ACCEPTED,
            stripe_payment_id="pi_test123",
        )

        self.app.set_user(self.student.username)
        with patch.object(stripe.Refund, "create") as mock_refund:
            mock_refund.return_value = MagicMock()
            response = self.app.post(
                reverse("purchases:create_refund"),
                params={"course_id": self.course.id},
            )

        self.assertEqual(response.status_code, 201)
        self.assertIn("HX-Redirect", response.headers)
        self.assertIn(reverse("courses:course_purchased_list"), response.headers["HX-Redirect"])

    def test_refund_nonexistent_purchase_returns_404(self):
        self.app.set_user(self.student.username)
        response = self.app.post(
            reverse("purchases:create_refund"),
            params={"course_id": self.course.id},
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 404)


class PublisherIncomeIntegrationTests(WebTest):
    csrf_checks = False

    def setUp(self):
        self.publisher = get_user_model().objects.create_user(
            username="publisher",
            email="publisher@example.com",
            password="publisher-pass",  # noqa: S106
        )
        add_course_perm = Permission.objects.get(codename="add_course")
        self.publisher.user_permissions.add(add_course_perm)

        self.other_publisher = get_user_model().objects.create_user(
            username="other",
            email="other@example.com",
            password="other-pass",  # noqa: S106
        )
        self.other_publisher.user_permissions.add(add_course_perm)

        self.student = get_user_model().objects.create_user(
            username="student",
            email="student@example.com",
            password="student-pass",  # noqa: S106
        )

        self.course1 = Course.objects.create(
            name="Course 1",
            description="First course",
            price=25.00,
            is_draft=False,
            publisher=self.publisher,
        )
        self.course2 = Course.objects.create(
            name="Course 2",
            description="Second course",
            price=50.00,
            is_draft=False,
            publisher=self.publisher,
        )
        self.free_course = Course.objects.create(
            name="Free Course",
            description="No price",
            price=0,
            is_draft=False,
            publisher=self.publisher,
        )
        self.other_course = Course.objects.create(
            name="Other Publisher Course",
            description="Not publisher's course",
            price=100.00,
            is_draft=False,
            publisher=self.other_publisher,
        )

    def test_publisher_income_requires_login(self):
        response = self.app.get(
            reverse("purchases:publisher_income"),
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.location)

    def test_publisher_income_requires_permission(self):
        self.app.set_user(self.student.username)
        response = self.app.get(
            reverse("purchases:publisher_income"),
            expect_errors=True,
        )

        self.assertEqual(response.status_code, 403)

    def test_publisher_income_shows_only_own_courses(self):
        Purchase.objects.create(
            user=self.student,
            course=self.course1,
            amount=25.00,
            state=Purchase.State.ACCEPTED,
        )
        Purchase.objects.create(
            user=self.student,
            course=self.other_course,
            amount=100.00,
            state=Purchase.State.ACCEPTED,
        )

        self.app.set_user(self.publisher.username)
        response = self.app.get(reverse("purchases:publisher_income"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("Course 1", response.text)
        self.assertNotIn("Other Publisher Course", response.text)

    def test_publisher_income_shows_totals(self):
        Purchase.objects.create(
            user=self.student,
            course=self.course1,
            amount=25.00,
            state=Purchase.State.ACCEPTED,
        )
        Purchase.objects.create(
            user=self.student,
            course=self.course2,
            amount=50.00,
            state=Purchase.State.ACCEPTED,
        )
        Purchase.objects.create(
            user=self.student,
            course=self.free_course,
            amount=0,
            state=Purchase.State.ACCEPTED,
        )

        self.app.set_user(self.publisher.username)
        response = self.app.get(reverse("purchases:publisher_income"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("75", response.text)
        self.assertIn("3", response.text)
        self.assertIn("2", response.text)

    def test_publisher_income_excludes_non_accepted_purchases(self):
        Purchase.objects.create(
            user=self.student,
            course=self.course1,
            amount=25.00,
            state=Purchase.State.ACCEPTED,
        )
        Purchase.objects.create(
            user=self.student,
            course=self.course2,
            amount=50.00,
            state=Purchase.State.REFUSED,
        )
        Purchase.objects.create(
            user=self.student,
            course=self.free_course,
            amount=0,
            state=Purchase.State.PENDING,
        )

        self.app.set_user(self.publisher.username)
        response = self.app.get(reverse("purchases:publisher_income"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("Course 1", response.text)
        self.assertNotIn("Course 2", response.text)
        self.assertNotIn("Free Course", response.text)
        self.assertIn("25", response.text)
