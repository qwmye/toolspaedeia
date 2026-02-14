from django.urls import path

from .views import CourseDetailView
from .views import CourseListView
from .views import ModuleDetailView

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course_list"),
    path("<pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("modules/<pk>/", ModuleDetailView.as_view(), name="module_detail"),
]
