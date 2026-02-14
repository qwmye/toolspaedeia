from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.html import format_html
from django.views.generic import DetailView
from django.views.generic import ListView

from courses.models import Course
from courses.models import Module
from toolspaedeia.mixins import TitledViewMixin
from toolspaedeia.utils import markdown_to_html


class CourseDetailView(TitledViewMixin, LoginRequiredMixin, DetailView):
    model = Course
    context_object_name = "course"
    login_url = "users:login"

    def get_title(self):
        """Return the course name as the title."""
        return self.get_object().name


class CourseListView(TitledViewMixin, LoginRequiredMixin, ListView):
    model = Course
    context_object_name = "courses"
    title = "Course List"
    login_url = "users:login"


class ModuleDetailView(TitledViewMixin, LoginRequiredMixin, DetailView):
    model = Module
    context_object_name = "module"
    login_url = "users:login"

    def get_title(self):
        """Return the module title and course name as the title."""
        return f"{self.get_object().title} | {self.get_object().course.name}"

    def get_context_data(self, **kwargs):
        """Add the module content in HTML format to the context."""
        context = super().get_context_data(**kwargs)
        context["content"] = format_html(markdown_to_html(self.object.content or ""))
        return context
