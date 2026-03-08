# Register your models here.

from django.contrib import admin

from .models import Answer
from .models import Course
from .models import Module
from .models import ModuleProgression
from .models import Question
from .models import Quiz
from .models import Resource


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "publisher", "is_draft"]
    list_filter = ["is_draft"]


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    search_fields = ["title", "course__name"]
    list_display = ["title", "course", "order", "is_draft"]
    list_filter = ["is_draft"]
    inlines = [ResourceInline]
    ordering = ["course", "order"]


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


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ["title", "module", "file"]
    search_fields = ["title", "module__title"]
