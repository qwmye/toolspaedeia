from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Course(models.Model):
    """Model representing a course in the Paedeia system."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    publisher = models.ForeignKey(
        get_user_model(), related_name="published_courses", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        """Meta class for the Course model."""

        permissions = [
            ("publish_course", "Can publish course"),
        ]

    def __str__(self) -> str:
        return self.name


class Module(models.Model):
    """Model representing a module within a course."""

    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.title


class ModuleProgression(models.Model):
    """Model representing a user's progression through a module."""

    user = models.ForeignKey(get_user_model(), related_name="module_progressions", on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name="progressions", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Meta class for the ModuleProgression model."""

        unique_together = ("user", "module")

    def __str__(self) -> str:
        return f"{self.user.username} - {self.module.title} - {'Completed' if self.completed else 'In Progress'}"

    def mark_completed(self):
        """Mark the module as completed."""
        self.completed = True
        self.completion_date = timezone.now()
        self.save()

    def mark_in_progress(self):
        """Mark the module as in progress."""
        self.completed = False
        self.completion_date = None
        self.save()
