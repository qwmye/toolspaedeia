from django.urls import path

from .views import VisualizerView

urlpatterns = [
    path("visualize/", VisualizerView.as_view(), name="visualizer"),
]
