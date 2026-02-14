from django.contrib.auth import views as auth_views
from django.urls import path

from users.views import UserPreferencesView

app_name = "users"

urlpatterns = [
    path("switch-theme/", UserPreferencesView.as_view(), name="switch_theme"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
