# Register your models here.

from common.services import markdown_to_html
from django.contrib import admin
from django.utils.html import format_html

from .models import Course
from .models import Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model."""

    list_display = ("name", "start_date", "end_date")
    search_fields = ("name",)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Admin interface for Module model."""

    list_display = ("title", "course")
    search_fields = ("title",)
    list_filter = ("course",)
    fields = ("course", "title", "content", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj: Module | None = None):
        """Get the HTML preview of the module content."""
        if not obj:
            return ""
        return format_html(markdown_to_html(obj.content))
