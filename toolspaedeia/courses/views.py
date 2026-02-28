from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.html import format_html
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from courses.models import Course
from courses.models import Module
from courses.models import Quiz
from courses.service import build_checked_answers_data
from courses.service import build_quiz_data
from courses.service import get_attempt_questions
from courses.service import get_quiz_and_course
from courses.service import render_quiz_section
from toolspaedeia.mixins import TitledViewMixin
from toolspaedeia.utils import markdown_to_html


class CourseDetailView(TitledViewMixin, LoginRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"

    def get_title(self):
        """Return the course name as the title."""
        return self.get_object().name

    def get_context_data(self, **kwargs):
        """Add the list of modules and progress to the context."""
        context_data = super().get_context_data(**kwargs)
        modules = list(self.object.modules.all())
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
        context_data["user_is_publisher"] = self.request.user == self.object.publisher or self.request.user.is_superuser
        return context_data


class CourseUserListView(TitledViewMixin, LoginRequiredMixin, ListView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "courses"
    title = "My Courses"
    template_name = "courses/courses_user_list.html"
    login_url = "users:login"

    def get_queryset(self):
        """Return the list of courses the user is enrolled in."""
        if self.request.user.is_superuser:
            return Course.objects.exclude(publisher=self.request.user)
        return Course.objects.filter(purchases__user=self.request.user).distinct()

    def get_context_data(self, *args, **kwargs):
        """
        Add the list of published courses and permission to publish course to
        the context.
        """
        context_data = super().get_context_data(*args, **kwargs)
        context_data["published_courses"] = Course.objects.filter(publisher=self.request.user)
        return context_data


class CourseBrowseListView(TitledViewMixin, LoginRequiredMixin, ListView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "courses"
    title = "Browse Courses"
    template_name = "courses/courses_browse_list.html"
    login_url = "users:login"

    def get_context_data(self, *args, **kwargs):
        """
        Add a additional details to the course to indicating whether the user
        has purchased it.
        """
        context_data = super().get_context_data(*args, **kwargs)
        for course in context_data["courses"]:
            if self.request.user.is_superuser or course.publisher == self.request.user:
                course.is_purchased = True
            else:
                course.is_purchased = course.purchases.filter(user=self.request.user).exists()
        return context_data


class CourseModuleDetailView(TitledViewMixin, LoginRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"
    template_name = "courses/course_module_detail.html"

    def get_object(self, queryset=None):
        """Return the course object with the specified module."""
        course = super().get_object(queryset)
        module_id = self.kwargs.get("module_id")
        if module_id:
            course.module = course.modules.get(id=module_id)
        return course

    def get_title(self):
        """Return the module title and course name as the title."""
        course = self.get_object()
        return f"{course.module.title} | {course.name}"

    def get_context_data(self, **kwargs):
        """Add the module content in HTML format to the context."""
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        module = course.module
        previous_module = self.object.modules.filter(order__lt=module.order).order_by("-order").first()
        next_module = self.object.modules.filter(order__gt=module.order).order_by("order").first()
        if previous_module:
            context["previous_module"] = previous_module
        if next_module:
            context["next_module"] = next_module
        module.is_completed = module.progressions.filter(user=self.request.user, completed=True).exists()
        context["module"] = module
        context["content"] = format_html(markdown_to_html(module.content or ""))

        try:
            module_quiz = module.quiz
        except Quiz.DoesNotExist:
            module_quiz = None

        context["module_quiz"] = module_quiz
        context["module_quiz_data"] = (
            build_quiz_data(list(module_quiz.get_questions_for_attempt())) if module_quiz else []
        )

        return context


class ModuleMarkCompleteView(LoginRequiredMixin, UpdateView):
    http_method_names = ["post"]
    model = Module
    pk_url_kwarg = "module_id"
    context_object_name = "module"
    login_url = "users:login"
    fields = []

    def get_success_url(self) -> str:
        """Redirect the user to the module detail page."""
        return reverse("courses:course_detail", kwargs={"course_id": self.object.course.id})

    def post(self, request, *args, **kwargs):
        """Toggle the completion status of the module for the user."""
        module = self.get_object()
        progression, _ = module.progressions.get_or_create(user=request.user)
        progression.completed = not progression.completed
        progression.save()
        return super().post(request, *args, **kwargs)


class CheckQuizView(LoginRequiredMixin, View):
    """View for checking quiz answers and reloading the quiz."""

    login_url = "users:login"

    def get(self, request, course_id, quiz_id):
        """Reload quiz with fresh questions."""
        quiz, course = get_quiz_and_course(course_id, quiz_id)
        questions = get_attempt_questions(quiz)
        quiz_data = build_quiz_data(questions)
        return render_quiz_section(request, quiz, course, quiz_data, show_results=False)

    def post(self, request, course_id, quiz_id):
        """Check submitted quiz answers and return quiz with feedback."""
        quiz, course = get_quiz_and_course(course_id, quiz_id)
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
        return render_quiz_section(request, quiz, course, quiz_data, show_results=True)
