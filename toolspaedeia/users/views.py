from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
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
    tags_paginate_by = 3

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

    def _build_pagination_context(self, page_obj, page_param, tag_query):
        query_suffix = f"&q={tag_query}" if tag_query else ""
        context = {"page_obj": page_obj, "page_param": page_param}
        if page_obj.has_previous():
            context["previous_url"] = f"?{page_param}={page_obj.previous_page_number()}{query_suffix}"
        if page_obj.has_next():
            context["next_url"] = f"?{page_param}={page_obj.next_page_number()}{query_suffix}"
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_query = self.get_tag_query()
        available_page_obj = self.get_available_tag_page_obj()
        preferred_page_obj = self.get_preferred_tag_page_obj()
        available_ctx = self._build_pagination_context(available_page_obj, "available_page", tag_query)
        preferred_ctx = self._build_pagination_context(preferred_page_obj, "preferred_page", tag_query)
        context["available_tags_page_obj"] = available_page_obj
        context["preferred_tags_page_obj"] = preferred_page_obj
        context["tag_query"] = tag_query
        context["query_suffix"] = f"?q={tag_query}" if tag_query else ""
        context["available_previous_url"] = available_ctx.get("previous_url")
        context["available_next_url"] = available_ctx.get("next_url")
        context["preferred_previous_url"] = preferred_ctx.get("previous_url")
        context["preferred_next_url"] = preferred_ctx.get("next_url")
        return context

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.request.get_full_path())


class ToggleTagPreferenceView(LoginRequiredMixin, View):
    http_method_names = ["post"]
    login_url = "users:login"

    def post(self, request):
        tag_id = request.POST.get("tag_id")
        if not tag_id:
            return HttpResponse("Missing tag_id", status=400)

        tag = get_object_or_404(CourseTag, id=tag_id)
        preferences, _ = UserSitePreferences.objects.get_or_create(user=request.user)

        if preferences.preferred_tags.filter(id=tag.id).exists():
            preferences.preferred_tags.remove(tag)
        else:
            preferences.preferred_tags.add(tag)

        tag_query = request.GET.get("q", "").strip()
        available_page_obj = self._get_available_tag_page_obj(preferences)
        preferred_page_obj = self._get_preferred_tag_page_obj(preferences)
        query_suffix = f"&q={tag_query}" if tag_query else ""
        context = {
            "available_tags_page_obj": available_page_obj,
            "preferred_tags_page_obj": preferred_page_obj,
            "tag_query": tag_query,
            "query_suffix": f"?q={tag_query}" if tag_query else "",
            "available_previous_url": f"?available_page={available_page_obj.previous_page_number()}{query_suffix}"
            if available_page_obj.has_previous()
            else None,
            "available_next_url": f"?available_page={available_page_obj.next_page_number()}{query_suffix}"
            if available_page_obj.has_next()
            else None,
            "preferred_previous_url": f"?preferred_page={preferred_page_obj.previous_page_number()}{query_suffix}"
            if preferred_page_obj.has_previous()
            else None,
            "preferred_next_url": f"?preferred_page={preferred_page_obj.next_page_number()}{query_suffix}"
            if preferred_page_obj.has_next()
            else None,
        }
        html = render_to_string("users/partials/tags_lists.html", context, request=request)
        return HttpResponse(html)

    def _get_available_tag_page_obj(self, preferences):
        preferred_tag_ids = preferences.preferred_tags.values_list("id", flat=True)
        queryset = CourseTag.objects.exclude(id__in=preferred_tag_ids).order_by("name")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        paginator = Paginator(queryset, 3)
        return paginator.get_page(1)

    def _get_preferred_tag_page_obj(self, preferences):
        queryset = preferences.preferred_tags.all().order_by("name")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        paginator = Paginator(queryset, 3)
        return paginator.get_page(1)


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
