from django.contrib.auth import views as auth_views
from django.urls import path

from users.views import PurchaseCourseView
from users.views import UserAccountView
from users.views import UserProfileView
from users.views import UserSettingsView

app_name = "users"

urlpatterns = [
    path("account/", UserAccountView.as_view(), name="account"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("preferences/", UserProfileView.as_view(), name="profile"),
    path("purchase-course/", PurchaseCourseView.as_view(), name="purchase_course"),
    path("settings/", UserSettingsView.as_view(), name="settings"),
]
