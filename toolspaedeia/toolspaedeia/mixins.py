class TitledViewMixin:
    title = None

    def get_title(self):
        return self.title

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["title"] = self.get_title()
        return context_data
