import nested_admin
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.validators import FileExtensionValidator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path
from django.urls import reverse

from .imports import create_course_from_import
from .models import Answer
from .models import Course
from .models import Module
from .models import ModuleProgression
from .models import Question
from .models import Quiz
from .models import QuizAttempt
from .models import Resource

admin.site.site_title = "Toolspaedeia Publishing"
admin.site.site_header = "Toolspaedeia Publishing"
admin.site.index_title = "Toolspaedeia Publishing"


class ResourceInline(nested_admin.NestedStackedInline):
    model = Resource
    extra = 0


class ModuleInlineAdmin(nested_admin.NestedStackedInline):
    model = Module
    ordering = ["order"]
    inlines = [ResourceInline]
    extra = 0


@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "publisher", "is_draft"]
    list_filter = ["is_draft"]
    inlines = [ModuleInlineAdmin]
    change_list_template = "admin/courses/course/change_list.html"

    class CourseImportForm(forms.Form):
        markdown_file = forms.FileField(
            label="Markdown file",
            validators=[FileExtensionValidator(allowed_extensions=["md", "markdown", "txt"])],
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import/", self.admin_site.admin_view(self.import_course_view), name="courses_course_import"),
        ]
        return custom_urls + urls

    def import_course_view(self, request):
        if not self.has_add_permission(request):
            raise PermissionDenied

        form = self.CourseImportForm(request.POST or None, request.FILES or None)

        if request.method == "POST" and form.is_valid():
            markdown_file = form.cleaned_data["markdown_file"]
            try:
                markdown_input = markdown_file.read().decode("utf-8")
            except UnicodeDecodeError:
                self.message_user(
                    request,
                    "Could not decode file as UTF-8. Please upload a UTF-8 markdown file.",
                    level=messages.ERROR,
                )
            else:
                try:
                    course = create_course_from_import(markdown_input, request.user)
                except ValueError as exc:
                    self.message_user(request, str(exc), level=messages.ERROR)
                else:
                    self.message_user(request, "Course imported successfully.")
                    change_url = reverse("admin:courses_course_change", args=[course.pk])
                    return HttpResponseRedirect(change_url)

        context = {
            **self.admin_site.each_context(request),
            "opts": self.opts,
            "title": "Import course",
            "form": form,
        }
        return TemplateResponse(request, "admin/courses/course/import_course.html", context)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(publisher=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.publisher = request.user
        super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields.remove("publisher")
        return fields


class AnswerInlineAdmin(nested_admin.NestedTabularInline):
    model = Answer
    extra = 0


class QuestionInlineAdmin(nested_admin.NestedStackedInline):
    model = Question
    ordering = ["order"]
    inlines = [AnswerInlineAdmin]
    extra = 0


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ["title", "module", "randomize_questions", "track_attempts", "max_questions", "max_attempts"]
    list_select_related = ["module"]
    inlines = [QuestionInlineAdmin]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(module__course__publisher=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "module" and not request.user.is_superuser:
            kwargs["queryset"] = Module.objects.filter(course__publisher=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ModuleProgression)
class ModuleProgressionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "module", "completed"]
    list_select_related = ["module"]
    list_filter = ["completed"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(module__course__publisher=request.user)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "quiz", "grade", "completion_date"]
    list_select_related = ["quiz"]
    list_filter = ["completion_date"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(quiz__module__course__publisher=request.user)
