from django.urls import path

from .views import CourseDetailView
from .views import CourseListView

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course_list"),
    path("<pk>/", CourseDetailView.as_view(), name="course_detail"),
]
