from django.urls import path

from .views import AttemptQuizView
from .views import CourseBrowseListView
from .views import CourseDetailView
from .views import CourseModuleDetailView
from .views import CoursePublishedListView
from .views import CoursePurchasedListView
from .views import CourseRecommendationsListView
from .views import ModuleMarkCompleteView

app_name = "courses"

urlpatterns = [
    path("browse/", CourseBrowseListView.as_view(), name="course_browse_list"),
    path("purchased-courses/", CoursePurchasedListView.as_view(), name="course_purchased_list"),
    path("published-courses/", CoursePublishedListView.as_view(), name="course_published_list"),
    path("recommendations/", CourseRecommendationsListView.as_view(), name="course_recommendations_list"),
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
]
