import nested_admin
from django.contrib import admin

from .models import Answer
from .models import Course
from .models import Module
from .models import ModuleProgression
from .models import Question
from .models import Quiz
from .models import QuizAttempt
from .models import Resource


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
    list_display = ["title", "module", "randomize_questions", "max_questions"]
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
