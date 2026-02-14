from django.utils.html import format_html
from django.views.generic import DetailView
from django.views.generic import ListView

from courses.models import Course
from toolspaedeia.utils import markdown_to_html


class CourseDetailView(DetailView):
    model = Course
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        """Add the course modules in HTML format to the context."""
        context = super().get_context_data(**kwargs)
        context["modules"] = {
            module: format_html(markdown_to_html(module.content)) for module in self.object.modules.all()
        }
        return context


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
