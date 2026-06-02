from datetime import timedelta
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import Q
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from courses.markdown import markdown_to_html
from courses.models import Course
from courses.models import Module
from courses.models import Quiz
from courses.models import QuizAttempt
from courses.quizzes import build_checked_answers_data
from courses.quizzes import build_quiz_data
from courses.quizzes import calculate_final_grade
from courses.quizzes import get_attempt_questions
from purchases.models import Purchase
from toolspaedeia.mixins import TitledViewMixin


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
        is_purchase_refundable = False
        purchase: Purchase | None = Purchase.objects.filter(user=self.request.user, course=self.object).first()
        if purchase:
            is_purchase_refundable = purchase.purchase_date + timedelta(days=1) > timezone.now()

        context_data["modules"] = modules
        context_data["total_modules"] = len(modules)
        context_data["progress"] = progress
        context_data["progress_percentage"] = (
            (context_data["progress"] / context_data["total_modules"] * 100) if modules else 0
        )
        context_data["user_is_publisher"] = self.request.user == self.object.publisher
        context_data["user_can_refund"] = not context_data["user_is_publisher"] and is_purchase_refundable
        context_data["course_tags"] = {
            tag.name: tag.preferred_by_users.filter(id=self.request.user.id).exists() for tag in self.object.tags.all()
        }
        return context_data


class CourseBaseListView(TitledViewMixin, LoginRequiredMixin, ListView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "courses"
    login_url = "users:login"
    template_name = "courses/course_list.html"
    htmx_template_name = "courses/partials/course_article_list.html"
    empty_message = "No courses available."
    paginate_by = 5

    def get_template_names(self):
        if self.request.headers.get("HX-Request") == "true":
            return [self.htmx_template_name]
        return [self.template_name]

    def get_search_query(self):
        return self.request.GET.get("q", "").strip()

    def apply_search(self, queryset):
        query = self.get_search_query()
        if not query:
            return queryset
        return queryset.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(publisher__first_name__icontains=query)
            | Q(publisher__last_name__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()

    def get_base_queryset(self):
        return Course.objects.none()

    def get_queryset(self):
        return self.apply_search(self.get_base_queryset()).order_by("id")

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["query"] = self.get_search_query()
        context_data["empty_message"] = self.empty_message
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
            course.course_tags = {
                tag.name: tag.preferred_by_users.filter(id=self.request.user.id).exists() for tag in course.tags.all()
            }
        return context_data


class CoursePurchasedListView(CourseBaseListView):
    title = "Purchased Courses"
    empty_message = "No courses purchased yet."

    def get_base_queryset(self):
        return Course.objects.filter(
            purchases__user=self.request.user, purchases__state=Purchase.State.ACCEPTED
        ).distinct()


class CoursePublishedListView(CourseBaseListView):
    title = "My Courses"
    empty_message = "No courses published yet."

    def get_base_queryset(self):
        return Course.objects.filter(publisher=self.request.user)


class CourseBrowseListView(CourseBaseListView):
    title = "Browse Courses"

    def get_base_queryset(self):
        return Course.objects.filter(is_draft=False)


class CourseRecommendationsListView(CourseBaseListView):
    title = "Recommended Courses"
    empty_message = "No recommendations available. Explore more courses or set your preferred tags!"

    def get_base_queryset(self):
        user_preferences = self.request.user.preferences
        preferred_tag_ids = set(user_preferences.preferred_tags.values_list("id", flat=True))

        purchased_tag_ids = set(
            self.request.user.purchases.filter(state=Purchase.State.ACCEPTED).values_list("course__tags__id", flat=True)
        )

        unpurchased_courses = (
            Course.objects.filter(is_draft=False)
            .exclude(purchases__user=self.request.user, purchases__state=Purchase.State.ACCEPTED)
            .exclude(publisher=self.request.user)
            .prefetch_related("tags")
            .distinct()
        )

        scored_courses = []
        for course in unpurchased_courses:
            course_tag_ids = {tag.id for tag in course.tags.all()}
            score = len(course_tag_ids & preferred_tag_ids) * 2 + len(course_tag_ids & purchased_tag_ids)
            if score > 0:
                scored_courses.append((score, course.id))

        scored_courses.sort(reverse=True)
        top_course_ids = [course_id for _, course_id in scored_courses[:5]]

        return Course.objects.filter(id__in=top_course_ids).prefetch_related("tags")


class CourseModuleDetailView(TitledViewMixin, LoginRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"
    template_name = "courses/course_module_detail.html"

    def get_queryset(self) -> QuerySet[Course]:
        queryset = super().get_queryset()
        return queryset.filter(
            Q(publisher=self.request.user)
            | Q(is_draft=False, purchases__user=self.request.user, purchases__state=Purchase.State.ACCEPTED)
        ).distinct()

    def get_object(self, queryset=None) -> Course:
        course = super().get_object(queryset)
        module_id = self.kwargs.get("module_id")
        if module_id:
            user_is_publisher = self.request.user == course.publisher
            draft_filter = Q() if user_is_publisher else Q(is_draft=False)
            course.module = course.modules.filter(draft_filter).get(id=module_id)
        return course

    def get_title(self) -> str:
        course = self.get_object()
        return f"{course.module.title}"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        module = course.module
        context["user_is_publisher"] = self.request.user == course.publisher

        user_is_publisher = context["user_is_publisher"]
        draft_filter = Q() if user_is_publisher else Q(is_draft=False)

        previous_module = (
            self.object.modules.filter(order__lt=module.order).filter(draft_filter).order_by("-order").first()
        )
        next_module = self.object.modules.filter(order__gt=module.order).filter(draft_filter).order_by("order").first()
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
        course = get_object_or_404(Course, id=course_id, modules__id=module_id)

        user_is_publisher = request.user == course.publisher
        has_access = (
            user_is_publisher
            or course.purchases.filter(
                user=request.user,
                state=Purchase.State.ACCEPTED,
            ).exists()
        )

        if not has_access:
            return HttpResponse(status=403)

        module = get_object_or_404(Module, pk=module_id, course=course)
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

        user_is_publisher = request.user == course.publisher
        has_access = (
            user_is_publisher
            or course.purchases.filter(
                user=request.user,
                state=Purchase.State.ACCEPTED,
            ).exists()
        )

        if not has_access:
            return HttpResponse(status=403)

        questions = get_attempt_questions(quiz)
        quiz_data = build_quiz_data(questions)
        return self.render_quiz_section(request, quiz, course, quiz_data)

    def post(self, request, course_id, quiz_id):
        quiz = get_object_or_404(
            Quiz.objects.select_related("module__course"),
            id=quiz_id,
            module__course_id=course_id,
        )
        course = quiz.module.course

        user_is_publisher = request.user == course.publisher
        has_access = (
            user_is_publisher
            or course.purchases.filter(
                user=request.user,
                state=Purchase.State.ACCEPTED,
            ).exists()
        )

        if not has_access:
            return HttpResponse(status=403)

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
