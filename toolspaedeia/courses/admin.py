# Register your models here.

from django.contrib import admin

from .models import Course
from .models import Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    search_fields = ("name",)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    search_fields = ("title",)
    list_filter = ("course",)
