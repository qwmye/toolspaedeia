from django.urls import path

from purchases.views import CreateRefundView
from purchases.views import EnrollCourseView
from purchases.views import EnrollmentDialogView
from purchases.views import PublisherIncomeView
from purchases.views import PurchasedContentOfflineMapView
from purchases.views import StripeWebhookView

app_name = "purchases"

urlpatterns = [
    path("income/", PublisherIncomeView.as_view(), name="publisher_income"),
    path("offline-map/", PurchasedContentOfflineMapView.as_view(), name="offline_map"),
    path("enrollment-dialog/", EnrollmentDialogView.as_view(), name="enrollment_dialog"),
    path("enroll-course/", EnrollCourseView.as_view(), name="enroll_course"),
    path("create-refund/", CreateRefundView.as_view(), name="create_refund"),
    path("stripe/webhook/", StripeWebhookView.as_view(), name="stripe_webhook"),
]
