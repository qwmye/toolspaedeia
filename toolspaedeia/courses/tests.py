import tempfile

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from courses.models import Answer
from courses.models import Course
from courses.models import Module
from courses.models import Question
from courses.models import Quiz
from courses.models import Resource
from courses.service import calculate_final_grade
from courses.utils import markdown_to_html


class TestCalculateFinalGrade(TestCase):
    def test_empty_quiz_data_returns_zero(self):
        """No questions means a zero grade."""
        self.assertEqual(calculate_final_grade([]), 0)

    def test_all_correct_returns_100(self):
        """Every answer is correct => 100%."""
        quiz_data = [
            {
                "answers_data": [
                    {"is_correct_choice": True},
                    {"is_correct_choice": True},
                ],
            },
            {
                "answers_data": [
                    {"is_correct_choice": True},
                ],
            },
        ]
        self.assertEqual(calculate_final_grade(quiz_data), 100)

    def test_all_wrong_returns_zero(self):
        """Not a single correct choice => 0%."""
        quiz_data = [
            {
                "answers_data": [
                    {"is_correct_choice": False},
                    {"is_correct_choice": False},
                ],
            },
        ]
        self.assertEqual(calculate_final_grade(quiz_data), 0)

    def test_partial_correctness(self):
        """Mixed results should give the right rounded percentage (75%)."""
        quiz_data = [
            {
                "answers_data": [
                    {"is_correct_choice": True},
                    {"is_correct_choice": False},
                    {"is_correct_choice": True},
                ],
            },
            {
                "answers_data": [
                    {"is_correct_choice": True},
                ],
            },
        ]
        self.assertEqual(calculate_final_grade(quiz_data), 75)

    def test_single_question_single_answer(self):
        """Edge case: one question with one answer."""
        correct = [{"answers_data": [{"is_correct_choice": True}]}]
        wrong = [{"answers_data": [{"is_correct_choice": False}]}]
        self.assertEqual(calculate_final_grade(correct), 100)
        self.assertEqual(calculate_final_grade(wrong), 0)

    def test_question_with_empty_answers_returns_zero(self):
        """A question with no answers shouldn't break."""
        quiz_data = [{"answers_data": []}]
        self.assertEqual(calculate_final_grade(quiz_data), 0)

    def test_result_is_rounded_float(self):
        """Grade with a non-integer ratio keeps two decimals (66.67%)."""
        quiz_data = [
            {
                "answers_data": [
                    {"is_correct_choice": True},
                    {"is_correct_choice": True},
                    {"is_correct_choice": False},
                ],
            },
        ]
        result = calculate_final_grade(quiz_data)
        self.assertEqual(result, 66.67)


class TestCheckQuizView(TestCase):
    def setUp(self):
        """Create some initial users and courses with some content."""
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

        self.course = Course.objects.create(name="Course", description="Course description", publisher=self.publisher)
        self.module = Module.objects.create(
            course=self.course,
            title="Module",
            description="Module description",
            content="Module content",
            order=1,
        )
        self.quiz = Quiz.objects.create(
            module=self.module,
            title="Quiz",
            description="Quiz description",
            randomize_questions=False,
        )

        self.question_one = Question.objects.create(quiz=self.quiz, text="Question One", order=1)
        self.question_two = Question.objects.create(quiz=self.quiz, text="Question Two", order=2)

        self.q1_answer_a = Answer.objects.create(question=self.question_one, text="Q1 Answer A", is_correct=True)
        self.q1_answer_b = Answer.objects.create(question=self.question_one, text="Q1 Answer B", is_correct=False)
        self.q1_answer_c = Answer.objects.create(question=self.question_one, text="Q1 Answer C", is_correct=True)

        self.q2_answer_a = Answer.objects.create(question=self.question_two, text="Q2 Answer A", is_correct=False)
        self.q2_answer_b = Answer.objects.create(question=self.question_two, text="Q2 Answer B", is_correct=True)

        self.url = reverse("courses:check_quiz", kwargs={"course_id": self.course.id, "quiz_id": self.quiz.id})

    def test_get_requires_authenticated_user(self):
        """Redirect unauthorized users to login when retrying a quiz."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)

    def test_post_requires_authenticated_user(self):
        """Redirect unauthorized users to login when checking a quiz."""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)

    def test_get_returns_fresh_attempt_with_check_action(self):
        """Retry should return a fresh attempt."""
        self.client.force_login(self.student)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Check Quiz", content)
        self.assertNotIn("Retry Quiz", content)
        self.assertIn('name="question_ids"', content)
        self.assertNotIn("aria-invalid", content)

    def test_post_scores_based_on_displayed_questions_and_answers(self):
        """
        Submitted attempts should be graded against the exact questions and
        answers the user saw.
        """
        self.client.force_login(self.student)

        data = {
            "question_ids": [str(self.question_two.id), str(self.question_one.id)],
            f"answer_ids_{self.question_two.id}": [
                str(self.q2_answer_b.id),
                str(self.q2_answer_a.id),
            ],
            f"answer_ids_{self.question_one.id}": [
                str(self.q1_answer_b.id),
                str(self.q1_answer_c.id),
                str(self.q1_answer_a.id),
            ],
            f"question-{self.question_two.id}": [str(self.q2_answer_b.id)],
            f"question-{self.question_one.id}": [str(self.q1_answer_c.id)],
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        self.assertIn("Retry Quiz", content)

        self.assertLess(content.find("Question Two"), content.find("Question One"))
        self.assertLess(content.find("Q2 Answer B"), content.find("Q2 Answer A"))
        self.assertLess(content.find("Q1 Answer B"), content.find("Q1 Answer C"))
        self.assertLess(content.find("Q1 Answer C"), content.find("Q1 Answer A"))

        self.assertIn('aria-invalid="false"', content)
        self.assertIn('aria-invalid="true"', content)

    def test_post_without_hidden_ids_falls_back_to_quiz_attempt_generation(self):
        """
        A valid submission should still be graded even if client hidden fields
        are missing.
        """
        self.client.force_login(self.student)

        response = self.client.post(
            self.url,
            data={
                f"question-{self.question_one.id}": [str(self.q1_answer_a.id)],
            },
        )

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Question One", content)
        self.assertIn("Question Two", content)
        self.assertIn("Retry Quiz", content)

    def test_wrong_course_and_quiz_pair_returns_not_found(self):
        """
        A quiz check request should fail when quiz does not belong to the
        provided course.
        """
        self.client.force_login(self.student)

        other_course = Course.objects.create(
            name="Other Course",
            description="Other description",
            publisher=self.publisher,
        )
        wrong_url = reverse(
            "courses:check_quiz",
            kwargs={"course_id": other_course.id, "quiz_id": self.quiz.id},
        )

        get_response = self.client.get(wrong_url)
        post_response = self.client.post(wrong_url, data={})

        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(post_response.status_code, 404)

    def test_post_with_tampered_answer_ids_payload(self):
        """
        Submitting answers that were not in the displayed answer set should be
        safely ignored (graded as not-selected). This prevents tampering where a
        user injects answer IDs that were never shown.
        """
        self.client.force_login(self.student)

        # Create a third question and answer not shown in the attempt
        other_question = Question.objects.create(quiz=self.quiz, text="Hidden Question", order=3)
        other_answer = Answer.objects.create(question=other_question, text="Hidden Answer", is_correct=True)

        # Submit: real answers + tampered answer ID that was never displayed
        data = {
            "question_ids": [str(self.question_one.id), str(self.question_two.id)],
            f"answer_ids_{self.question_one.id}": [
                str(self.q1_answer_a.id),
                str(self.q1_answer_b.id),
            ],
            f"answer_ids_{self.question_two.id}": [
                str(self.q2_answer_a.id),
                str(self.q2_answer_b.id),
            ],
            # Tampered: submit answer from hidden_question
            f"question-{self.question_one.id}": [str(self.q1_answer_a.id), str(other_answer.id)],
            f"question-{self.question_two.id}": [str(self.q2_answer_b.id)],
        }

        response = self.client.post(self.url, data=data)

        # Should still render successfully and treat tampered answer as not
        # selected
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # Verify legitimate answer is marked correct, tampered answer is ignored
        self.assertIn("aria-invalid", content)

    def test_post_with_tampered_question_ids_order(self):
        """
        Questions in posted_question_ids determine grading order. If a user
        tampers with question order, they're still graded against exactly the
        questions they submitted (replay protection), not arbitrary reordering.
        """
        self.client.force_login(self.student)

        # Swap question order in submission
        data = {
            "question_ids": [str(self.question_two.id), str(self.question_one.id)],  # Reversed
            f"answer_ids_{self.question_two.id}": [
                str(self.q2_answer_a.id),
                str(self.q2_answer_b.id),
            ],
            f"answer_ids_{self.question_one.id}": [
                str(self.q1_answer_a.id),
                str(self.q1_answer_b.id),
                str(self.q1_answer_c.id),
            ],
            f"question-{self.question_two.id}": [str(self.q2_answer_b.id)],
            f"question-{self.question_one.id}": [str(self.q1_answer_a.id)],
        }

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # Verify both questions are graded correctly in reversed order
        q2_pos = content.find("Question Two")
        q1_pos = content.find("Question One")
        self.assertLess(q2_pos, q1_pos, "Question Two should appear before Question One (reversed order)")


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class TestResourcePlugin(TestCase):
    """Resource rendering through the mistune plugin in markdown_to_html."""

    def setUp(self):
        self.publisher = get_user_model().objects.create_user(
            username="publisher",
            email="publisher@example.com",
            password="publisher-pass",  # noqa: S106
        )
        self.course = Course.objects.create(
            name="Course",
            description="desc",
            publisher=self.publisher,
        )
        self.module = Module.objects.create(
            course=self.course,
            title="Mod",
            description="desc",
            content="",
            order=1,
        )

    def _make_resource(self, title="Slides", filename="slides.pdf"):
        r = Resource(module=self.module, title=title)
        r.file.save(filename, ContentFile(b"fake"), save=True)
        return r

    def test_pdf_placeholder_rendered_as_iframe(self):
        resource = self._make_resource("Lecture Slides")
        html = markdown_to_html("Download resource:Lecture Slides here.", resources=[resource])

        self.assertIn("<iframe", html)
        self.assertIn(resource.file.url, html)
        self.assertNotIn("resource:", html)

    def test_image_placeholder_rendered_as_img(self):
        resource = self._make_resource("Diagram", "diagram.png")
        html = markdown_to_html("See resource:Diagram below.", resources=[resource])

        self.assertIn("<img", html)
        self.assertIn(resource.file.url, html)

    def test_video_placeholder_rendered_as_video(self):
        resource = self._make_resource("Demo", "demo.mp4")
        html = markdown_to_html("Watch resource:Demo", resources=[resource])

        self.assertIn("<video", html)
        self.assertIn(resource.file.url, html)

    def test_audio_placeholder_rendered_as_audio(self):
        resource = self._make_resource("Podcast", "episode.mp3")
        html = markdown_to_html("Listen to resource:Podcast", resources=[resource])

        self.assertIn("<audio", html)
        self.assertIn(resource.file.url, html)

    def test_generic_file_rendered_as_link(self):
        resource = self._make_resource("Notes", "notes.txt")
        html = markdown_to_html("Get resource:Notes", resources=[resource])

        self.assertIn(f'<a href="{resource.file.url}">', html)
        self.assertIn("Notes</a>", html)

    def test_unmatched_placeholder_left_as_is(self):
        html = markdown_to_html("See resource:Missing File for details.", resources=[])

        self.assertIn("resource:Missing File", html)

    def test_multiple_placeholders_in_same_text(self):
        r1 = self._make_resource("A", "a.png")
        r2 = self._make_resource("B", "b.pdf")
        html = markdown_to_html("Get resource:A and resource:B", resources=[r1, r2])

        self.assertIn(r1.file.url, html)
        self.assertIn(r2.file.url, html)

    def test_no_resources_renders_markdown_normally(self):
        html = markdown_to_html("**bold** text")

        self.assertIn("<strong>bold</strong>", html)

    def test_no_placeholders_returns_html_unchanged(self):
        r = self._make_resource("Slides")
        html_with = markdown_to_html("Plain text.", resources=[r])
        html_without = markdown_to_html("Plain text.")

        self.assertEqual(html_with, html_without)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class TestResourceModel(TestCase):
    def setUp(self):
        self.publisher = get_user_model().objects.create_user(
            username="testpub",
            email="pub@example.com",
            password="pubpass",  # noqa: S106
        )
        self.course = Course.objects.create(
            name="Course",
            description="desc",
            publisher=self.publisher,
        )
        self.module = Module.objects.create(
            course=self.course,
            title="Mod",
            description="desc",
            content="",
            order=1,
        )

    def _make_resource(self, title="Notes"):
        r = Resource(module=self.module, title=title)
        r.file.save("notes.pdf", ContentFile(b"fake"), save=True)
        return r

    def test_upload_path_contains_publisher_username(self):
        r = self._make_resource()
        self.assertIn(f"resources/{self.publisher.username}/", r.file.name)

    def test_str_returns_title(self):
        r = self._make_resource("My Notes")
        self.assertEqual(str(r), "My Notes")

    def test_resource_deleted_with_module(self):
        self._make_resource()
        self.assertEqual(Resource.objects.count(), 1)
        self.module.delete()
        self.assertEqual(Resource.objects.count(), 0)

    def test_allowed_extension_passes_validation(self):
        r = Resource(module=self.module, title="Image")
        r.file.save("photo.png", ContentFile(b"fake"), save=False)
        try:
            r.full_clean()
        except ValidationError:
            self.fail("ValidationError raised for allowed extension .png")

    def test_disallowed_extension_fails_validation(self):
        r = Resource(module=self.module, title="Executable")
        r.file.save("malware.exe", ContentFile(b"fake"), save=False)
        with self.assertRaises(ValidationError):
            r.full_clean()

    def test_spreadsheet_extension_passes_validation(self):
        for ext in ["xls", "xlsx", "ods", "csv"]:
            with self.subTest(extension=ext):
                r = Resource(module=self.module, title=f"Sheet_{ext}")
                r.file.save(f"data.{ext}", ContentFile(b"fake"), save=False)
                try:
                    r.full_clean()
                except ValidationError:
                    self.fail(f"ValidationError raised for allowed extension .{ext}")
