from django.urls import path

from purchases.views import CreateCheckoutSessionView
from purchases.views import PublisherIncomeView
from purchases.views import PurchaseCourseView
from purchases.views import PurchasedContentOfflineMapView
from purchases.views import StripeWebhookView

app_name = "purchases"

urlpatterns = [
    path("income/", PublisherIncomeView.as_view(), name="publisher_income"),
    path("offline-map/", PurchasedContentOfflineMapView.as_view(), name="offline_map"),
    path("purchase-course/", PurchaseCourseView.as_view(), name="purchase_course"),
    path("create-checkout-session/", CreateCheckoutSessionView.as_view(), name="create_checkout_session"),
    path("stripe/webhook/", StripeWebhookView.as_view(), name="stripe_webhook"),
]
