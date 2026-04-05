from django.urls import path

from .stripe_checkout import create_checkout_session
from .views import AttemptQuizView
from .views import CourseBrowseListView
from .views import CourseDetailView
from .views import CourseModuleDetailView
from .views import CourseUserListView
from .views import ModuleMarkCompleteView

app_name = "courses"

urlpatterns = [
    path("browse/", CourseBrowseListView.as_view(), name="course_browse_list"),
    path("my-courses/", CourseUserListView.as_view(), name="course_user_list"),
    path("<int:course_id>/", CourseDetailView.as_view(), name="course_detail"),
    path("<int:course_id>/modules/<int:module_id>/", CourseModuleDetailView.as_view(), name="module_detail"),
    path(
        "<int:course_id>/modules/<int:module_id>/mark-complete/",
        ModuleMarkCompleteView.as_view(),
        name="module_mark_complete",
    ),
    path(
        "<int:course_id>/quiz/<int:quiz_id>/attempt/",
        AttemptQuizView.as_view(),
        name="attempt_quiz",
    ),
    path("create-checkout-session/", create_checkout_session, name="create_checkout_session"),
]
