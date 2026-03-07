from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import UpdateView

from users.forms import AccountForm
from users.models import Purchase
from users.models import UserSettings
from users.models import UserSitePreferences


class UserProfileView(LoginRequiredMixin, UpdateView):
    """View to display and update user site preferences."""

    model = UserSitePreferences
    fields = ["color_theme", "theme_mode"]
    template_name = "users/preferences.html"
    success_url = reverse_lazy("users:profile")
    login_url = reverse_lazy("users:login")

    def get_object(self, _queryset=None):
        """Return the current user's preferences, creating them if needed."""
        obj, _ = UserSitePreferences.objects.get_or_create(user=self.request.user)
        return obj


class UserSettingsView(LoginRequiredMixin, UpdateView):
    """View to display and update user settings."""

    model = UserSettings
    fields = ["profile_picture", "receive_notifications"]
    template_name = "users/settings.html"
    success_url = reverse_lazy("users:settings")
    login_url = reverse_lazy("users:login")

    def get_object(self, _queryset=None):
        """Return the current user's settings, creating them if needed."""
        obj, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return obj


class PurchaseCourseView(LoginRequiredMixin, CreateView):
    """View to handle course purchases."""

    http_method_names = ["post"]
    model = Purchase
    fields = ["course"]
    login_url = reverse_lazy("users:login")
    success_url = reverse_lazy("courses:course_browse_list")

    def form_valid(self, form):
        """Handle valid form submission for course purchase."""
        Purchase.objects.get_or_create(
            user=self.request.user,
            course=form.instance.course,
            defaults={"amount": form.instance.course.price},
        )
        return redirect(self.request.META.get("HTTP_REFERER", self.success_url))


class UserAccountView(LoginRequiredMixin, UpdateView):
    """View to update username, email, and password."""

    model = get_user_model()
    form_class = AccountForm
    template_name = "users/account.html"
    success_url = reverse_lazy("users:account")
    login_url = reverse_lazy("users:login")

    def get_object(self, _queryset=None):
        """Return the current user."""
        return self.request.user

    def form_valid(self, form):
        """Save changes and keep the user logged in if the password changed."""
        user = form.save()
        update_session_auth_hash(self.request, user)
        return redirect(self.success_url)
