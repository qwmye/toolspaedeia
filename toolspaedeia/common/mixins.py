class TitledViewMixin:
    """Mixin for views that have a title."""

    title = None

    def get_title(self):
        """Get the title of the view."""
        return self.title

    def get_context_data(self, *args, **kwargs):
        """Add the title to the context."""
        context_data = super().get_context_data(*args, **kwargs)
        context_data["title"] = self.get_title()
        return context_data
