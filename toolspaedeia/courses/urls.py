from django.urls import path

from .views import CourseDetailView
from .views import CourseModuleDetailView
from .views import UserCourseListView

app_name = "courses"

urlpatterns = [
    path("", UserCourseListView.as_view(), name="user_course_list"),
    path("<course_id>/", CourseDetailView.as_view(), name="course_detail"),
    path("<course_id>/modules/<module_id>/", CourseModuleDetailView.as_view(), name="module_detail"),
]
