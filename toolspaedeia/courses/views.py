from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import Q
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from courses.markdown import markdown_to_html
from courses.models import Course
from courses.models import Module
from courses.models import Quiz
from courses.models import QuizAttempt
from courses.service import build_checked_answers_data
from courses.service import build_quiz_data
from courses.service import calculate_final_grade
from courses.service import get_attempt_questions
from toolspaedeia.mixins import TitledViewMixin
from users.models import Purchase


class CourseDetailView(TitledViewMixin, LoginRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"

    def get_title(self):
        return self.get_object().name

    def get_queryset(self) -> QuerySet[Course]:
        queryset = super().get_queryset()
        return queryset.filter(
            Q(publisher=self.request.user)
            | Q(is_draft=False, purchases__user=self.request.user, purchases__state=Purchase.State.ACCEPTED)
        ).distinct()

    def get_context_data(self, **kwargs):
        """Add the list of modules and progress to the context."""
        context_data = super().get_context_data(**kwargs)
        if self.request.user == self.object.publisher:
            modules = list(self.object.modules.order_by("order"))
        else:
            modules = list(self.object.modules.filter(is_draft=False).order_by("order"))
        progress = 0
        for module in modules:
            module.is_completed = module.progressions.filter(user=self.request.user, completed=True).exists()
            if module.is_completed:
                progress += 1
        context_data["modules"] = modules
        context_data["total_modules"] = len(modules)
        context_data["progress"] = progress
        context_data["progress_percentage"] = (
            (context_data["progress"] / context_data["total_modules"] * 100) if modules else 0
        )
        context_data["user_is_publisher"] = self.request.user == self.object.publisher
        return context_data


class CourseBaseListView(TitledViewMixin, LoginRequiredMixin, ListView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "courses"
    login_url = "users:login"
    template_name = "courses/course_list.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        for course in context_data["courses"]:
            if course.publisher == self.request.user:
                course.is_purchased = True
                course.is_payment_pending = False
                course.has_refused_payment = False
            else:
                user_purchases = course.purchases.filter(user=self.request.user)
                course.is_purchased = user_purchases.filter(state=Purchase.State.ACCEPTED).exists()
                course.is_payment_pending = user_purchases.filter(state=Purchase.State.PENDING).exists()
                course.has_refused_payment = user_purchases.filter(state=Purchase.State.REFUSED).exists()
        return context_data


class CoursePurchasedListView(CourseBaseListView):
    title = "Purchased Courses"

    def get_queryset(self):
        return Course.objects.filter(
            purchases__user=self.request.user,
            purchases__state=Purchase.State.ACCEPTED,
        ).distinct()


class CoursePublishedListView(CourseBaseListView):
    title = "Published Courses"

    def get_queryset(self):
        return Course.objects.filter(publisher=self.request.user)


class CourseBrowseListView(CourseBaseListView):
    title = "Browse Courses"
    queryset = Course.objects.filter(is_draft=False)


class CourseModuleDetailView(TitledViewMixin, LoginRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"
    template_name = "courses/course_module_detail.html"

    def get_queryset(self) -> QuerySet[Course]:
        """Return the course with the specified module, if it is not a draft."""
        queryset = super().get_queryset()
        return queryset.filter(
            Q(publisher=self.request.user)
            | Q(is_draft=False, purchases__user=self.request.user, purchases__state=Purchase.State.ACCEPTED)
        ).distinct()

    def get_object(self, queryset=None) -> Course:
        course = super().get_object(queryset)
        module_id = self.kwargs.get("module_id")
        if module_id:
            course.module = course.modules.filter(Q(is_draft=False) | Q(course__publisher=self.request.user)).get(
                id=module_id
            )
        return course

    def get_title(self) -> str:
        course = self.get_object()
        return f"{course.module.title}"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        module = course.module
        context["user_is_publisher"] = self.request.user == course.publisher
        previous_module = self.object.modules.filter(order__lt=module.order).order_by("-order").first()
        next_module = self.object.modules.filter(order__gt=module.order).order_by("order").first()
        if previous_module:
            context["previous_module"] = previous_module
        if next_module:
            context["next_module"] = next_module
        module.is_completed = module.progressions.filter(user=self.request.user, completed=True).exists()
        context["module"] = module

        resources = list(module.resources.all())
        context["resources"] = resources

        content_md = module.content or ""
        context["content"] = mark_safe(markdown_to_html(content_md, resources=resources))  # noqa: S308

        try:
            module_quiz = module.quiz
        except Quiz.DoesNotExist:
            module_quiz = None

        context["module_quiz"] = module_quiz

        return context


class ModuleMarkCompleteView(LoginRequiredMixin, View):
    http_method_names = ["post"]
    login_url = "users:login"

    def post(self, request, course_id, module_id):
        """Toggle the completion status of the module for the user."""
        module = get_object_or_404(Module, pk=module_id)
        progression, _ = module.progressions.get_or_create(user=request.user)
        progression.completed = not progression.completed
        progression.save()
        context = {
            "course_id": course_id,
            "module_id": module_id,
            "completed": progression.completed,
            "show_message": True,
        }
        html = render_to_string("courses/partials/mark_complete_button.html", context, request=request)
        return HttpResponse(html)


class AttemptQuizView(LoginRequiredMixin, View):
    login_url = "users:login"

    @staticmethod
    def render_quiz_section(request, quiz, course, quiz_data, final_grade=None):
        """Render quiz section partial HTML response."""
        quiz_attempts = list(quiz.attempts.filter(user=request.user).order_by("-completion_date"))
        best_quiz_attempt_grade = max(
            (attempt.grade for attempt in quiz_attempts if attempt.grade is not None), default=None
        )
        context = {
            "quiz": quiz,
            "course": course,
            "quiz_data": quiz_data,
            "final_grade": final_grade,
            "quiz_attempts": quiz_attempts,
            "best_quiz_attempt_grade": best_quiz_attempt_grade,
        }
        html = render_to_string("courses/partials/quiz_section.html", context, request=request)
        return HttpResponse(html)

    def get(self, request, course_id, quiz_id):
        quiz = get_object_or_404(
            Quiz.objects.select_related("module__course"),
            id=quiz_id,
            module__course_id=course_id,
        )
        course = quiz.module.course
        questions = get_attempt_questions(quiz)
        quiz_data = build_quiz_data(questions)
        return self.render_quiz_section(request, quiz, course, quiz_data)

    def post(self, request, course_id, quiz_id):
        """Check submitted quiz answers and return quiz with feedback."""
        quiz = get_object_or_404(
            Quiz.objects.select_related("module__course"),
            id=quiz_id,
            module__course_id=course_id,
        )
        course = quiz.module.course
        questions = get_attempt_questions(quiz, request.POST.getlist("question_ids"))

        answers_by_question = {}
        for question in questions:
            submitted_answer_ids = set(request.POST.getlist(f"question-{question.id}"))
            posted_answer_ids = request.POST.getlist(f"answer_ids_{question.id}")
            answers_by_question[question.id] = build_checked_answers_data(
                question,
                submitted_answer_ids,
                posted_answer_ids,
            )

        quiz_data = build_quiz_data(questions, answers_by_question=answers_by_question)
        final_grade = calculate_final_grade(quiz_data)
        if quiz.track_attempts:
            QuizAttempt.objects.create(user=request.user, quiz=quiz, grade=str(final_grade))
        return self.render_quiz_section(request, quiz, course, quiz_data, final_grade=final_grade)
