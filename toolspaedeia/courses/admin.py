# Register your models here.

from django.contrib import admin

from .models import Course
from .models import Module
from .models import ModuleProgression


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model."""


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Admin interface for Module model."""


@admin.register(ModuleProgression)
class ModuleProgressionAdmin(admin.ModelAdmin):
    """Admin interface for ModuleProgression model."""
