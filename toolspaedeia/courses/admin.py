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
    search_fields = ["name"]
    list_display = ["name", "publisher", "is_draft"]
    list_filter = ["is_draft"]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    search_fields = ["title", "course__name"]
    list_display = ["title", "course", "order", "is_draft"]
    list_filter = ["is_draft"]


@admin.register(ModuleProgression)
class ModuleProgressionAdmin(admin.ModelAdmin):
    pass


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
