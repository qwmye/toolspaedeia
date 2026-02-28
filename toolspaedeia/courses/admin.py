# Register your models here.

from django.contrib import admin

from .models import Answer
from .models import Course
from .models import Module
from .models import ModuleProgression
from .models import Question
from .models import Quiz


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model."""

    search_fields = ["name"]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Admin interface for Module model."""

    search_fields = ["title", "course__name"]
    list_display = ["title", "course", "order"]


@admin.register(ModuleProgression)
class ModuleProgressionAdmin(admin.ModelAdmin):
    """Admin interface for ModuleProgression model."""


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin interface for Quiz model."""


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question model."""


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin interface for Answer model."""
