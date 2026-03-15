"""
URL configuration for toolspaedeia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path("", include("pwa.urls")),
    path("", RedirectView.as_view(pattern_name="courses:course_browse_list"), name="home"),
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
    path("users/", include("users.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
