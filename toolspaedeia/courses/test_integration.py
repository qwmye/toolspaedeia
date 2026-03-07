from django.contrib.auth import get_user_model
from django.urls import reverse
from django_webtest import WebTest

from courses.models import Answer
from courses.models import Course
from courses.models import Module
from courses.models import ModuleProgression
from courses.models import Question
from courses.models import Quiz
from users.models import Purchase


class CoursesIntegrationWebTests(WebTest):
    csrf_checks = False

    def setUp(self):
        """
        Create initial course with two modules (one with a quiz)
        and a student.
        """
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
            name="Integration Course",
            description="Course description",
            is_draft=False,
            price=19.99,
            publisher=self.publisher,
        )
        self.module_intro = Module.objects.create(
            course=self.course,
            title="Introduction",
            description="Introduction module",
            content="Hello module",
            order=1,
            is_draft=False,
        )
        self.module_quiz = Module.objects.create(
            course=self.course,
            title="Quiz Module",
            description="Quiz module",
            content="Quiz content",
            order=2,
            is_draft=False,
        )

        self.quiz = Quiz.objects.create(
            module=self.module_quiz,
            title="Module Quiz",
            description="Quick check",
            randomize_questions=False,
        )
        self.question = Question.objects.create(quiz=self.quiz, text="What is 2 + 2?", order=1)
        self.correct_answer = Answer.objects.create(question=self.question, text="4", is_correct=True)
        self.wrong_answer = Answer.objects.create(question=self.question, text="5", is_correct=False)

        Purchase.objects.create(user=self.student, course=self.course, amount=self.course.price)

        self.bug_course = Course.objects.create(
            name="Duplicate Purchase Course",
            description="Course for duplicate purchase bug coverage",
            is_draft=False,
            price=5.00,
            publisher=self.publisher,
        )

    def login_through_form(self):
        """Log the student in via the login form and follow redirects."""
        self.app.reset()
        login_page = self.app.get(reverse("users:login"))
        login_form = login_page.form
        login_form["username"] = self.student.username
        login_form["password"] = "student-pass"  # noqa: S105
        response = login_form.submit()
        while response.status_code in {301, 302, 303, 307, 308}:
            response = response.follow()
        return response

    def test_course_browse_list_navigation(self):
        """
        Browse page lists available courses with purchase state.

        Actions:
            Login and land on browse.
        Behaviour:
            Page renders the public course catalogue.
        Expectation:
            Purchased course shows "Go to Course" link, unpurchased
            ones show a purchase button.
        """
        browse_page = self.login_through_form()

        self.assertEqual(browse_page.status_code, 200)
        self.assertIn("Integration Course", browse_page.text)
        self.assertIn("Go to Course", browse_page.text)
        self.assertIn("Duplicate Purchase Course", browse_page.text)
        self.assertIn("Purchase for", browse_page.text)

    def test_course_user_list_navigation(self):
        """
        My Courses page shows purchased and published sections.

        Actions:
            Login, click the "My Courses" nav link.
        Behaviour:
            Page renders with separate purchased/published headings.
        Expectation:
            Student sees the purchased course listed; the empty
            published section shows a placeholder message.
        """
        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))

        self.assertEqual(my_courses_page.status_code, 200)
        self.assertIn("Purchased Courses", my_courses_page.text)
        self.assertIn("Integration Course", my_courses_page.text)
        self.assertIn("Published Courses", my_courses_page.text)
        self.assertIn("No courses published yet.", my_courses_page.text)

    def test_course_detail_navigation(self):
        """
        Course detail page shows modules and a progress bar.

        Actions:
            Login, go to My Courses, click into the course.
        Behaviour:
            Detail page renders module list with progress summary.
        Expectation:
            Both module names are visible and progress starts at 0 out of 2.
        """
        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))
        detail_page = my_courses_page.click("Go to Course")

        self.assertEqual(detail_page.status_code, 200)
        self.assertIn("Integration Course", detail_page.text)
        self.assertIn("Introduction", detail_page.text)
        self.assertIn("Quiz Module", detail_page.text)
        self.assertIn("0 out of 2 modules completed", detail_page.text)

    def test_module_detail_navigation(self):
        """
        Opening a module from the course detail page.

        Actions:
            Login, navigate to course detail, click "Start" on the quiz module.
        Behaviour:
            Module page renders content, quiz section, and nav buttons.
        Expectation:
            Module title and quiz heading are visible.
        """
        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))
        detail_page = my_courses_page.click("Go to Course")
        module_page = detail_page.click("Start", index=1)

        self.assertEqual(module_page.status_code, 200)
        self.assertIn("Quiz Module", module_page.text)
        self.assertIn("Module Quiz", module_page.text)
        self.assertIn("Mark as Completed", module_page.text)

    def test_module_mark_complete_post_flow(self):
        """
        Marking a module as completed.

        Actions:
            Login, open the intro module, POST mark-complete.
        Behaviour:
            Progression row is created and marked completed;
            redirects back to course detail.
        Expectation:
            DB has completed=True for the student+module and
            course detail shows "1 out of 2".
        """
        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))
        detail_page = my_courses_page.click("Go to Course")
        detail_page.click("Start", index=0)

        mark_complete_url = reverse(
            "courses:module_mark_complete", kwargs={"course_id": self.course.id, "module_id": self.module_intro.id}
        )
        detail_page = self.app.post(mark_complete_url).follow()

        self.assertTrue(
            ModuleProgression.objects.filter(user=self.student, module=self.module_intro, completed=True).exists()
        )
        self.assertIn("1 out of 2 modules completed", detail_page.text)

    def test_module_mark_complete_toggles_back(self):
        """
        Marking complete twice toggles it back to incomplete.

        Actions:
            Login, POST mark-complete on intro module twice.
        Behaviour:
            First POST marks completed, second flips it back.
        Expectation:
            DB progression has completed=False after the second toggle;
            course detail shows 0 out of 2 again.
        """
        self.login_through_form()
        mark_url = reverse(
            "courses:module_mark_complete", kwargs={"course_id": self.course.id, "module_id": self.module_intro.id}
        )

        self.app.post(mark_url).follow()
        detail_page = self.app.post(mark_url).follow()

        self.assertTrue(
            ModuleProgression.objects.filter(user=self.student, module=self.module_intro, completed=False).exists()
        )
        self.assertIn("0 out of 2 modules completed", detail_page.text)

    def test_check_quiz_get_flow(self):
        """
        GET on the quiz check endpoint loads a fresh attempt.

        Actions:
            Login, navigate to quiz module, GET the check URL.
        Behaviour:
            Returns the quiz form in "check" mode (no results).
        Expectation:
            "Check Quiz" button visible, "Retry Quiz" is not.
        """
        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))
        detail_page = my_courses_page.click("Go to Course")
        detail_page.click("Start", index=1)

        check_url = reverse("courses:check_quiz", kwargs={"course_id": self.course.id, "quiz_id": self.quiz.id})
        response = self.app.get(check_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Check Quiz", response.text)
        self.assertNotIn("Retry Quiz", response.text)

    def test_check_quiz_post_flow(self):
        """
        Submitting quiz answers and seeing results.

        Actions:
            Login, navigate to quiz, POST with the correct answer selected.
        Behaviour:
            Server evaluates and returns result mode.
        Expectation:
            "Retry Quiz" button appears (results are shown).
        """
        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))
        detail_page = my_courses_page.click("Go to Course")
        detail_page.click("Start", index=1)
        check_url = reverse("courses:check_quiz", kwargs={"course_id": self.course.id, "quiz_id": self.quiz.id})
        response = self.app.post(
            check_url,
            params={
                "question_ids": [str(self.question.id)],
                f"answer_ids_{self.question.id}": [str(self.correct_answer.id), str(self.wrong_answer.id)],
                f"question-{self.question.id}": [str(self.correct_answer.id)],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Retry Quiz", response.text)

    def test_duplicate_purchase_is_idempotent(self):
        """
        Repeated purchase POSTs for same course don't duplicate.

        Actions:
            Login, purchase bug_course via form, then POST the
            same payload raw twice more.
        Behaviour:
            get_or_create silently skips duplicates.
        Expectation:
            Only one Purchase row in the DB.
        """
        browse_page = self.login_through_form()
        purchase_form = next(
            form
            for form in browse_page.forms.values()
            if (
                form.action.endswith(reverse("users:purchase_course"))
                and form.fields.get("course")
                and str(form["course"].value) == str(self.bug_course.id)
            )
        )

        purchase_form.submit().follow()

        purchase_url = reverse("users:purchase_course")

        self.app.post(purchase_url, params={"course": str(self.bug_course.id)})
        self.app.post(purchase_url, params={"course": str(self.bug_course.id)})

        self.assertEqual(Purchase.objects.filter(user=self.student, course=self.bug_course).count(), 1)

    def test_browse_page_requires_login(self):
        """
        Hitting /courses/browse/ without auth bounces to login.

        Actions:
            GET the browse URL without logging in.
        Behaviour:
            302 to login with a ?next= param.
        Expectation:
            Redirect location includes the login URL and the
            original browse path.
        """
        response = self.app.get(reverse("courses:course_browse_list"), expect_errors=True)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.location)
        self.assertIn("next=", response.location)

    def test_course_detail_nonexistent_course_returns_404(self):
        """
        Requesting a course ID that doesn't exist.

        Actions:
            Login, GET /courses/99999/.
        Behaviour:
            Django returns 404.
        Expectation:
            Status code is 404.
        """
        self.login_through_form()
        url = reverse("courses:course_detail", kwargs={"course_id": 99999})
        resp = self.app.get(url, expect_errors=True)

        self.assertEqual(resp.status_code, 404)

    def test_mark_complete_after_logout_redirects(self):
        """
        Stale mark-complete POST after session expired.

        Actions:
            Login, grab the mark-complete URL, logout, then POST it.
        Behaviour:
            Server redirects to login (LoginRequiredMixin).
        Expectation:
            Raise 302 to login, no progression row created.
        """
        self.login_through_form()
        mark_url = reverse(
            "courses:module_mark_complete", kwargs={"course_id": self.course.id, "module_id": self.module_intro.id}
        )

        self.app.post(reverse("users:logout"))
        resp = self.app.post(mark_url, expect_errors=True)

        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("users:login"), resp.location)
        self.assertFalse(ModuleProgression.objects.filter(user=self.student, module=self.module_intro).exists())

    def test_check_quiz_wrong_course_id_returns_404(self):
        """
        Quiz check URL with mismatched course ID.

        Actions:
            Login, POST quiz check with a course_id that doesn't own this quiz.
        Behaviour:
            get_object_or_404 rejects the mismatch.
        Expectation:
            Raise 404.
        """
        self.login_through_form()
        bad_url = reverse("courses:check_quiz", kwargs={"course_id": self.bug_course.id, "quiz_id": self.quiz.id})
        resp = self.app.get(bad_url, expect_errors=True)

        self.assertEqual(resp.status_code, 404)
