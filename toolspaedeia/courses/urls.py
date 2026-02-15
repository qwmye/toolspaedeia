from django.urls import path

from .views import CourseBrowseListView
from .views import CourseDeleteView
from .views import CourseDetailView
from .views import CourseModuleDetailView
from .views import CoursePublishView
from .views import CourseUpdateView
from .views import CourseUserListView
from .views import ModuleCreateView
from .views import ModuleDeleteView
from .views import ModuleMarkCompleteView
from .views import ModuleUpdateView

app_name = "courses"

urlpatterns = [
    path("browse/", CourseBrowseListView.as_view(), name="course_browse_list"),
    path("personal/", CourseUserListView.as_view(), name="course_user_list"),
    path("publish/", CoursePublishView.as_view(), name="course_publish"),
    path("<course_id>/view/", CourseDetailView.as_view(), name="course_detail"),
    path("<course_id>/update/", CourseUpdateView.as_view(), name="course_update"),
    path("<course_id>/delete/", CourseDeleteView.as_view(), name="course_delete"),
    path("<course_id>/add/", ModuleCreateView.as_view(), name="module_add"),
    path("<course_id>/view/<module_id>/", CourseModuleDetailView.as_view(), name="module_detail"),
    path("<course_id>/update/<module_id>", ModuleUpdateView.as_view(), name="module_update"),
    path("<course_id>/delete/<module_id>", ModuleDeleteView.as_view(), name="module_delete"),
    path("<course_id>/mark-complete/<module_id>", ModuleMarkCompleteView.as_view(), name="module_mark_complete"),
]
