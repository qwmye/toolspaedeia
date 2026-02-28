from django.urls import path

from .views import CourseBrowseListView
from .views import CourseDetailView
from .views import CourseModuleDetailView
from .views import CourseUserListView
from .views import ModuleMarkCompleteView

app_name = "courses"

urlpatterns = [
    path("browse/", CourseBrowseListView.as_view(), name="course_browse_list"),
    path("personal/", CourseUserListView.as_view(), name="course_user_list"),
    path("<course_id>/view/", CourseDetailView.as_view(), name="course_detail"),
    path("<course_id>/view/<module_id>/", CourseModuleDetailView.as_view(), name="module_detail"),
    path("<course_id>/mark-complete/<module_id>", ModuleMarkCompleteView.as_view(), name="module_mark_complete"),
]
