from django.urls import path

from .views import CourseDetailView
from .views import CourseListView
from .views import CourseModuleDetailView

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course_list"),
    path("<course_id>/", CourseDetailView.as_view(), name="course_detail"),
    path("<course_id>/modules/<module_id>/", CourseModuleDetailView.as_view(), name="module_detail"),
]
