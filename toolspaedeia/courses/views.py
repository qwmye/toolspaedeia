from django.utils.html import format_html
from django.views.generic import DetailView
from django.views.generic import ListView

from courses.models import Course
from courses.models import Module
from toolspaedeia.mixins import TitledViewMixin
from toolspaedeia.utils import markdown_to_html


class CourseDetailView(TitledViewMixin, DetailView):
    model = Course
    context_object_name = "course"
    title = "Course Details"


class CourseListView(TitledViewMixin, ListView):
    model = Course
    context_object_name = "courses"
    title = "Course List"


class ModuleDetailView(TitledViewMixin, DetailView):
    model = Module
    context_object_name = "module"
    title = "Module Details"

    def get_context_data(self, **kwargs):
        """Add the module content in HTML format to the context."""
        context = super().get_context_data(**kwargs)
        context["content"] = format_html(markdown_to_html(self.object.content or ""))
        return context
