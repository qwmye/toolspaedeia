from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import FormView

from users.models import Purchase
from users.models import UserPreferences


class UserProfileFormView(LoginRequiredMixin, FormView):
    class UserProfileModelForm(ModelForm):
        """Inline to update user preferences."""

        class Meta:
            """Meta class for user preferences inline form."""

            model = UserPreferences
            fields = ["profile_picture", "color_theme", "theme_mode"]

    form_class = UserProfileModelForm
    template_name = "profile.html"
    success_url = reverse_lazy("users:profile")

    def get_form_kwargs(self):
        """Get form kwargs for user profile form."""
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            preference, _ = UserPreferences.objects.get_or_create(user=self.request.user)
            kwargs["instance"] = preference
        return kwargs

    def form_valid(self, form):
        """Handle valid form submission for user profile form."""
        if not (self.request.user.is_authenticated and self.request.user.is_active):
            return HttpResponse("Unauthorized", status=401)

        form.save()
        return super().form_valid(form)


class PurchaseCourseView(LoginRequiredMixin, CreateView):
    """View to handle course purchases."""

    http_method_names = ["post"]
    model = Purchase
    fields = ["course"]
    success_url = reverse_lazy("courses:course_browse_list")

    def form_valid(self, form):
        """Handle valid form submission for course purchase."""
        if not (self.request.user.is_authenticated and self.request.user.is_active):
            return HttpResponse("Unauthorized", status=401)

        form.instance.user = self.request.user
        form.instance.amount = form.instance.course.price
        form.save()
        return redirect(self.request.META.get("HTTP_REFERER", self.success_url))
