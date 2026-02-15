from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from courses.models import Course
from courses.models import Module
from toolspaedeia.mixins import TitledViewMixin
from toolspaedeia.utils import markdown_to_html


class CoursePublishView(TitledViewMixin, LoginRequiredMixin, CreateView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"
    template_name = "courses/course_publish.html"
    title = "Publish Course"
    fields = ["name", "description", "price"]

    def get_success_url(self) -> str:
        """Redirect the user to the newly added course."""
        return reverse("courses:course_detail", kwargs={"course_id": self.object.id})

    def form_valid(self, form):
        """Set the publisher to the current user before saving the form."""
        form.instance.publisher = self.request.user
        return super().form_valid(form)


class CourseDetailView(TitledViewMixin, LoginRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"

    def get_title(self):
        """Return the course name as the title."""
        return self.get_object().name

    def get_context_data(self, **kwargs):
        """Add the list of modules and progress to the context."""
        context_data = super().get_context_data(**kwargs)
        modules = list(self.object.modules.order_by("order"))
        context_data["modules"] = modules
        context_data["progress"] = 0
        for module in modules:
            module.is_completed = module.progressions.filter(user=self.request.user, completed=True).exists()
            if module.is_completed:
                context_data["progress"] += 1
        context_data["progress_percentage"] = (context_data["progress"] / len(modules) * 100) if modules else 0
        context_data["user_is_publisher"] = self.request.user == self.object.publisher or self.request.user.is_superuser
        return context_data


class CourseUpdateView(TitledViewMixin, LoginRequiredMixin, UpdateView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"
    template_name = "courses/course_update.html"
    title = "Edit Course"
    fields = ["name", "description", "price"]

    def get_success_url(self) -> str:
        """Redirect the user to the updated course."""
        return reverse("courses:course_detail", kwargs={"course_id": self.object.id})


class CourseUserListView(TitledViewMixin, LoginRequiredMixin, ListView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "courses"
    title = "My Courses"
    template_name = "courses/courses_user_list.html"
    login_url = "users:login"

    def get_queryset(self):
        """Return the list of courses the user is enrolled in."""
        if self.request.user.is_superuser:
            return Course.objects.exclude(publisher=self.request.user)
        return Course.objects.filter(purchases__user=self.request.user).distinct()

    def get_context_data(self, *args, **kwargs):
        """
        Add the list of published courses and permission to publish course to
        the context.
        """
        context_data = super().get_context_data(*args, **kwargs)
        context_data["can_publish_course"] = self.request.user.has_perm("courses.publish_course")
        context_data["published_courses"] = Course.objects.filter(publisher=self.request.user)
        return context_data


class CourseBrowseListView(TitledViewMixin, LoginRequiredMixin, ListView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "courses"
    title = "Browse Courses"
    template_name = "courses/courses_browse_list.html"
    login_url = "users:login"

    def get_context_data(self, *args, **kwargs):
        """
        Add a additional details to the course to indicating whether the user
        has purchased it.
        """
        context_data = super().get_context_data(*args, **kwargs)
        for course in context_data["courses"]:
            if self.request.user.is_superuser or course.publisher == self.request.user:
                course.is_purchased = True
            else:
                course.is_purchased = course.purchases.filter(user=self.request.user).exists()
        return context_data


class CourseModuleDetailView(TitledViewMixin, LoginRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"
    template_name = "courses/course_module_detail.html"

    def get_object(self, queryset=None):
        """Return the course object with the specified module."""
        course = super().get_object(queryset)
        module_id = self.kwargs.get("module_id")
        if module_id:
            course.module = course.modules.get(id=module_id)
        return course

    def get_title(self):
        """Return the module title and course name as the title."""
        course = self.get_object()
        return f"{course.module.title} | {course.name}"

    def get_context_data(self, **kwargs):
        """Add the module content in HTML format to the context."""
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        module = course.module
        previous_module = self.object.modules.filter(order__lt=module.order).order_by("-order").first()
        next_module = self.object.modules.filter(order__gt=module.order).order_by("order").first()
        if previous_module:
            context["previous_module"] = previous_module
        if next_module:
            context["next_module"] = next_module
        context["module"] = module
        context["content"] = format_html(markdown_to_html(module.content or ""))
        return context


class CourseDeleteView(TitledViewMixin, LoginRequiredMixin, DeleteView):
    http_method_names = ["post"]
    model = Course
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"
    title = "Delete Course"
    success_url = reverse_lazy("courses:course_browse_list")


class ModuleCreateView(TitledViewMixin, LoginRequiredMixin, CreateView):
    model = Module
    pk_url_kwarg = "course_id"
    context_object_name = "course"
    login_url = "users:login"
    template_name = "courses/module_create.html"
    title = "Add Module"
    fields = ["title", "description", "content"]

    def get_success_url(self) -> str:
        """Redirect the user to the course page, to preview all modules."""
        return reverse("courses:course_detail", kwargs={"course_id": self.kwargs.get("course_id")})

    def get_context_data(self, *args, **kwargs):
        """Add the course in the context."""
        context_data = super().get_context_data(*args, **kwargs)
        course_id = self.kwargs.get("course_id")
        context_data["course"] = Course.objects.get(id=course_id)
        return context_data

    def form_valid(self, form):
        """Set the course to the current course before saving the form."""
        course_id = self.kwargs.get("course_id")
        form.instance.course_id = course_id
        try:
            form.instance.order = Course.objects.get(id=course_id).modules.latest("order").order + 1
        except Module.DoesNotExist:
            form.instance.order = 0
        return super().form_valid(form)


class ModuleUpdateView(TitledViewMixin, LoginRequiredMixin, UpdateView):
    model = Module
    pk_url_kwarg = "module_id"
    context_object_name = "module"
    login_url = "users:login"
    template_name = "courses/module_update.html"
    title = "Edit Module"
    fields = ["title", "description", "content"]

    def get_success_url(self) -> str:
        """Redirect the user to the course page, to preview all modules."""
        return reverse("courses:course_detail", kwargs={"course_id": self.object.course.id})


class ModuleDeleteView(TitledViewMixin, LoginRequiredMixin, DeleteView):
    http_method_names = ["post"]
    model = Module
    pk_url_kwarg = "module_id"
    context_object_name = "module"
    login_url = "users:login"
    title = "Delete Module"

    def get_success_url(self) -> str:
        """Redirect the user to the course page, to preview all modules."""
        return reverse("courses:course_detail", kwargs={"course_id": self.object.course.id})
