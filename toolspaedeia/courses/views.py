from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.html import format_html
from django.views.generic import DetailView
from django.views.generic import ListView

from courses.models import Course
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
        modules = list(self.object.modules.order_by("order"))
        context_data["modules"] = modules
        context_data["progress"] = 0
        return context_data


class UserCourseListView(TitledViewMixin, LoginRequiredMixin, ListView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "courses"
    title = "My Courses"
    template_name = "courses/user_courses.html"
    login_url = "users:login"

    def get_queryset(self):
        """Return the list of courses the user is enrolled in."""
        if self.request.user.is_superuser:
            return Course.objects.all()
        return Course.objects.filter(purchases__user=self.request.user).distinct()


class BrowseCourseListView(TitledViewMixin, LoginRequiredMixin, ListView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "courses"
    title = "Browse Courses"
    template_name = "courses/browse_courses.html"
    login_url = "users:login"

    def get_context_data(self, *args, **kwargs):
        """
        Add a additional details to the course to indicating whether the user
        has purchased it.
        """
        context_data = super().get_context_data(*args, **kwargs)
        for course in context_data["courses"]:
            if self.request.user.is_superuser:
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
        context["module"] = module
        context["content"] = format_html(markdown_to_html(module.content or ""))
        return context
