from django.contrib.auth import views as auth_views
from django.urls import path

from users.views import PublisherIncomeView
from users.views import PurchaseCourseView
from users.views import UserAccountView
from users.views import UserPreferencesView

app_name = "users"

urlpatterns = [
    path("account/", UserAccountView.as_view(), name="account"),
    path("income/", PublisherIncomeView.as_view(), name="publisher_income"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("preferences/", UserPreferencesView.as_view(), name="preferences"),
    path("purchase-course/", PurchaseCourseView.as_view(), name="purchase_course"),
]
