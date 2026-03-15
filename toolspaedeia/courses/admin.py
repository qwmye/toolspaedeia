# Register your models here.

import nested_admin
from django.contrib import admin

from .models import Answer
from .models import Course
from .models import Module
from .models import ModuleProgression
from .models import Question
from .models import Quiz
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
    inlines = [QuestionInlineAdmin]


@admin.register(ModuleProgression)
class ModuleProgressionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "module", "completed"]
    list_filter = ["completed"]
