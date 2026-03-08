import tempfile

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test.utils import override_settings
from django.urls import reverse
from django_webtest import WebTest

from courses.models import Answer
from courses.models import Course
from courses.models import Module
from courses.models import ModuleProgression
from courses.models import Question
from courses.models import Quiz
from courses.models import Resource
from users.models import Purchase


class CoursesWebTestBase(WebTest):
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


class PageLoadIntegrationTests(CoursesWebTestBase):
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
        self.assertIn("Mark as Complete", module_page.text)

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

    def test_module_page_no_message_on_first_load(self):
        """
        Initial module page load shows the button but no feedback message.

        Actions:
            Login, navigate to the intro module page.
        Behaviour:
            The mark-complete partial renders without the confirmation text.
        Expectation:
            "Mark as Complete" button is present; "Module marked as" is absent.
        """
        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))
        detail_page = my_courses_page.click("Go to Course")
        module_page = detail_page.click("Start", index=0)

        self.assertIn("Mark as Complete", module_page.text)
        self.assertNotIn("Module marked as", module_page.text)

    def test_module_page_no_message_when_already_completed(self):
        """
        Module page for an already-completed module hides the message.

        Actions:
            Mark the intro module complete, then reload the module page.
        Behaviour:
            The page shows the toggle button but no stale feedback text.
        Expectation:
            "Mark as Incomplete" button present; "Module marked as" absent.
        """
        ModuleProgression.objects.create(user=self.student, module=self.module_intro, completed=True)

        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))
        detail_page = my_courses_page.click("Go to Course")
        module_page = detail_page.click("Start", index=0)

        self.assertIn("Mark as Incomplete", module_page.text)
        self.assertNotIn("Module marked as", module_page.text)


class HtmxViewIntegrationTests(CoursesWebTestBase):
    """Tests that directly hit HTMX endpoints returning HTML fragments."""

    def test_mark_complete_post_flow(self):
        """
        Marking a module as completed via HTMX.

        Actions:
            Login, POST mark-complete on the intro module.
        Behaviour:
            Progression row is created and marked completed;
            returns updated button HTML.
        Expectation:
            DB has completed=True for the student+module and
            response contains the toggled button label.
        """
        self.login_through_form()
        mark_url = reverse(
            "courses:module_mark_complete", kwargs={"course_id": self.course.id, "module_id": self.module_intro.id}
        )
        response = self.app.post(mark_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ModuleProgression.objects.filter(user=self.student, module=self.module_intro, completed=True).exists()
        )
        self.assertIn("Mark as Incomplete", response.text)

    def test_mark_complete_toggles_back(self):
        """
        Marking complete twice toggles it back to incomplete.

        Actions:
            Login, POST mark-complete on intro module twice.
        Behaviour:
            First POST marks completed, second flips it back.
        Expectation:
            DB progression has completed=False after the second toggle
            and response shows the original button label.
        """
        self.login_through_form()
        mark_url = reverse(
            "courses:module_mark_complete", kwargs={"course_id": self.course.id, "module_id": self.module_intro.id}
        )

        first_response = self.app.post(mark_url)
        second_response = self.app.post(mark_url)

        self.assertEqual(first_response.status_code, 200)
        self.assertIn("Mark as Incomplete", first_response.text)
        self.assertEqual(second_response.status_code, 200)
        self.assertIn("Mark as Complete", second_response.text)
        self.assertTrue(
            ModuleProgression.objects.filter(user=self.student, module=self.module_intro, completed=False).exists()
        )

    def test_mark_complete_post_shows_message(self):
        """
        The feedback message appears only after the HTMX POST.

        Actions:
            Login, POST mark-complete on the intro module.
        Behaviour:
            The returned HTML fragment includes the confirmation text.
        Expectation:
            "Module marked as complete." is in the response.
        """
        self.login_through_form()
        mark_url = reverse(
            "courses:module_mark_complete", kwargs={"course_id": self.course.id, "module_id": self.module_intro.id}
        )
        response = self.app.post(mark_url)

        self.assertIn("Module marked as complete.", response.text)

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

    def test_mark_complete_get_not_allowed(self):
        """
        GET on the mark-complete endpoint isn't supported.

        Actions:
            Login, send a GET to the mark-complete URL.
        Behaviour:
            View only accepts POST (http_method_names).
        Expectation:
            Returns 405 Method Not Allowed.
        """
        self.login_through_form()
        mark_url = reverse(
            "courses:module_mark_complete", kwargs={"course_id": self.course.id, "module_id": self.module_intro.id}
        )
        resp = self.app.get(mark_url, expect_errors=True)

        self.assertEqual(resp.status_code, 405)

    def test_mark_complete_response_contains_htmx_attributes(self):
        """
        The returned button fragment should include hx-post for the
        next toggle.

        Actions:
            Login, POST mark-complete.
        Behaviour:
            Response is a standalone button with HTMX wiring.
        Expectation:
            HTML contains hx-post pointing back at the same URL
            and hx-swap="outerHTML".
        """
        self.login_through_form()
        mark_url = reverse(
            "courses:module_mark_complete", kwargs={"course_id": self.course.id, "module_id": self.module_intro.id}
        )
        resp = self.app.post(mark_url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(f'hx-post="{mark_url}"', resp.text)
        self.assertIn('hx-swap="outerHTML"', resp.text)

    def test_mark_complete_nonexistent_module_returns_404(self):
        """
        Marking a module that doesn't exist.

        Actions:
            Login, POST to mark-complete with a bogus module_id.
        Behaviour:
            Module.objects.get raises DoesNotExist.
        Expectation:
            Returns 404.
        """
        self.login_through_form()
        mark_url = reverse("courses:module_mark_complete", kwargs={"course_id": self.course.id, "module_id": 99999})
        resp = self.app.post(mark_url, expect_errors=True)

        self.assertEqual(resp.status_code, 404)

    def test_mark_complete_separate_users_independent(self):
        """
        Two users marking the same module don't interfere.

        Actions:
            Student marks intro complete, then a second user marks it too.
        Behaviour:
            Each gets their own ModuleProgression row.
        Expectation:
            Both progressions exist, both completed independently.
        """
        other_user = get_user_model().objects.create_user(
            username="other",
            email="other@example.com",
            password="other-pass",  # noqa: S106
        )
        Purchase.objects.create(user=other_user, course=self.course, amount=self.course.price)

        mark_url = reverse(
            "courses:module_mark_complete", kwargs={"course_id": self.course.id, "module_id": self.module_intro.id}
        )

        # Student marks complete
        self.login_through_form()
        self.app.post(mark_url)

        # Other user marks complete
        self.app.reset()
        login_page = self.app.get(reverse("users:login"))
        form = login_page.form
        form["username"] = "other"
        form["password"] = "other-pass"  # noqa: S105
        form.submit()
        self.app.post(mark_url)

        self.assertTrue(
            ModuleProgression.objects.filter(user=self.student, module=self.module_intro, completed=True).exists()
        )
        self.assertTrue(
            ModuleProgression.objects.filter(user=other_user, module=self.module_intro, completed=True).exists()
        )
        self.assertEqual(ModuleProgression.objects.filter(module=self.module_intro).count(), 2)

    def test_check_quiz_get_flow(self):
        """
        GET on the quiz check endpoint loads a fresh attempt.

        Actions:
            Login, GET the check URL.
        Behaviour:
            Returns the quiz form in "check" mode (no results).
        Expectation:
            "Check Quiz" button visible, "Retry Quiz" is not.
        """
        self.login_through_form()
        check_url = reverse("courses:check_quiz", kwargs={"course_id": self.course.id, "quiz_id": self.quiz.id})
        response = self.app.get(check_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Check Quiz", response.text)
        self.assertNotIn("Retry Quiz", response.text)

    def test_check_quiz_post_correct_answer(self):
        """
        Submitting quiz answers and seeing results with final grade.

        Actions:
            Login, POST with the correct answer selected.
        Behaviour:
            Server evaluates and returns result mode with a grade.
        Expectation:
            "Retry Quiz" button and "Final Grade: 100%" appear.
        """
        self.login_through_form()
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
        self.assertIn("Final Grade: 100.00%", response.text)

    def test_check_quiz_post_wrong_answer(self):
        """
        Submitting only the wrong answer produces a 0% grade.

        Actions:
            Login, POST quiz with only the wrong answer ticked.
        Behaviour:
            Both choices are wrong (wrong ticked, correct unticked).
        Expectation:
            Final grade is 0%.
        """
        self.login_through_form()
        check_url = reverse("courses:check_quiz", kwargs={"course_id": self.course.id, "quiz_id": self.quiz.id})
        response = self.app.post(
            check_url,
            params={
                "question_ids": [str(self.question.id)],
                f"answer_ids_{self.question.id}": [str(self.correct_answer.id), str(self.wrong_answer.id)],
                f"question-{self.question.id}": [str(self.wrong_answer.id)],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Final Grade: 0.00%", response.text)

    def test_check_quiz_get_has_no_final_grade(self):
        """
        A fresh quiz attempt shouldn't show any grade.

        Actions:
            Login, GET the quiz check endpoint.
        Behaviour:
            Returns quiz form without results.
        Expectation:
            "Final Grade" text is absent.
        """
        self.login_through_form()
        check_url = reverse("courses:check_quiz", kwargs={"course_id": self.course.id, "quiz_id": self.quiz.id})
        response = self.app.get(check_url)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Final Grade", response.text)

    def test_check_quiz_wrong_course_id_returns_404(self):
        """
        Quiz check URL with mismatched course ID.

        Actions:
            Login, GET quiz check with a course_id that doesn't own this quiz.
        Behaviour:
            get_object_or_404 rejects the mismatch.
        Expectation:
            Raise 404.
        """
        self.login_through_form()
        bad_url = reverse("courses:check_quiz", kwargs={"course_id": self.bug_course.id, "quiz_id": self.quiz.id})
        resp = self.app.get(bad_url, expect_errors=True)

        self.assertEqual(resp.status_code, 404)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ResourceIntegrationTests(CoursesWebTestBase):
    def _attach_resource(self, module, title="Handout", filename="handout.pdf"):
        r = Resource(module=module, title=title)
        r.file.save(filename, ContentFile(b"data"), save=True)
        return r

    def test_module_page_lists_resources_at_bottom(self):
        """
        Resources section appears when a module has attached files.

        Actions:
            Attach a resource to the intro module, login, navigate
            to the module page.
        Behaviour:
            Page renders the Resources heading with a download link.
        Expectation:
            Resource title and file URL both appear in the HTML.
        """
        resource = self._attach_resource(self.module_intro, "Lecture Notes")

        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))
        detail_page = my_courses_page.click("Go to Course")
        module_page = detail_page.click("Start", index=0)

        self.assertEqual(module_page.status_code, 200)
        self.assertIn("Resources", module_page.text)
        self.assertIn("Lecture Notes", module_page.text)
        self.assertIn(resource.file.url, module_page.text)

    def test_module_page_hides_resources_section_when_empty(self):
        """
        No Resources heading when module has no attached files.

        Actions:
            Login, navigate to the intro module (no resources).
        Behaviour:
            Page renders without the Resources section.
        Expectation:
            "Resources" heading is absent from the page.
        """
        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))
        detail_page = my_courses_page.click("Go to Course")
        module_page = detail_page.click("Start", index=0)

        self.assertNotIn("Resources", module_page.text)

    def test_inline_resource_placeholder_rendered_as_link(self):
        """
        resource:<title> in module content becomes a clickable link.

        Actions:
            Set module content with a resource:X placeholder, attach
            a matching resource, login, open the module page.
        Behaviour:
            Markdown renders the placeholder as an <a> link.
        Expectation:
            The raw placeholder text is gone, replaced by a link to
            the uploaded file.
        """
        self.module_intro.content = "Read the resource:Summary before continuing."
        self.module_intro.save()
        resource = self._attach_resource(self.module_intro, "Summary", "summary.pdf")

        browse_page = self.login_through_form()
        my_courses_page = browse_page.click(href=reverse("courses:course_user_list"))
        detail_page = my_courses_page.click("Go to Course")
        module_page = detail_page.click("Start", index=0)

        self.assertNotIn("resource:Summary", module_page.text)
        self.assertIn(resource.file.url, module_page.text)
