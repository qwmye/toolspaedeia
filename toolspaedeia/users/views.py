from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from courses.models import CourseTag
from users.forms import AccountForm
from users.models import UserSitePreferences


class UserPreferencesView(LoginRequiredMixin, UpdateView):
    model = UserSitePreferences
    fields = ["color_theme", "theme_mode", "profile_picture", "receive_notifications"]
    template_name = "users/preferences.html"
    htmx_template_name = "users/partials/tags_lists.html"
    success_url = reverse_lazy("users:preferences")
    login_url = "users:login"
    tags_paginate_by = 5

    def get_template_names(self):
        if self.request.headers.get("HX-Request") == "true":
            return [self.htmx_template_name]
        return [self.template_name]

    def get_object(self, _queryset=None):
        obj, _ = UserSitePreferences.objects.get_or_create(user=self.request.user)
        return obj

    def get_tag_query(self):
        return self.request.GET.get("q", "").strip()

    def get_preferred_tags_queryset(self):
        queryset = self.get_object().preferred_tags.all().order_by("name")
        query = self.get_tag_query()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_available_tag_queryset(self):
        preferred_tag_ids = self.get_preferred_tags_queryset().values_list("id", flat=True)
        queryset = CourseTag.objects.exclude(id__in=preferred_tag_ids)
        query = self.get_tag_query()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_available_tag_page_obj(self):
        paginator = Paginator(self.get_available_tag_queryset(), self.tags_paginate_by)
        return paginator.get_page(self.request.GET.get("available_page"))

    def get_preferred_tag_page_obj(self):
        paginator = Paginator(self.get_preferred_tags_queryset(), self.tags_paginate_by)
        return paginator.get_page(self.request.GET.get("preferred_page"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_tags_page_obj"] = self.get_available_tag_page_obj()
        context["preferred_tags_page_obj"] = self.get_preferred_tag_page_obj()
        context["tag_query"] = self.get_tag_query()
        return context

    def form_valid(self, form):
        self.object = form.save()

        preferred_tags_page_obj = self.get_preferred_tag_page_obj()
        visible_preferred_tag_ids = set(preferred_tags_page_obj.object_list.values_list("id", flat=True))
        kept_preferred_tag_ids = {
            int(tag_id) for tag_id in self.request.POST.getlist("preferred_tags") if tag_id.isdigit()
        }
        tags_to_remove = visible_preferred_tag_ids - kept_preferred_tag_ids
        if tags_to_remove:
            self.object.preferred_tags.remove(*tags_to_remove)

        available_tags_page_obj = self.get_available_tag_page_obj()
        available_page_tag_ids = set(available_tags_page_obj.object_list.values_list("id", flat=True))
        selected_available_tag_ids = {
            int(tag_id) for tag_id in self.request.POST.getlist("available_tags") if tag_id.isdigit()
        }
        tags_to_add = selected_available_tag_ids & available_page_tag_ids
        if tags_to_add:
            self.object.preferred_tags.add(*tags_to_add)

        return redirect(self.request.get_full_path())


class UserAccountView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = AccountForm
    template_name = "users/account.html"
    success_url = reverse_lazy("users:account")
    login_url = "users:login"

    def get_object(self, _queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return redirect(self.success_url)
