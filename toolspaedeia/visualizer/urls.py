from django.urls import path

from .views import VisualizerView, show_demo_svg

urlpatterns = [
    path("visualize/", VisualizerView.as_view(), name="visualizer"),
    path("visualize/ajax", show_demo_svg, name="visualizer-ajax"),
]
