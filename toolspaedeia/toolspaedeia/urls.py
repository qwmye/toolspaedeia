from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from toolspaedeia.views import HomeView

urlpatterns = [
    path("", include("pwa.urls")),
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
    path("purchases/", include("purchases.urls")),
    path("users/", include("users.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
