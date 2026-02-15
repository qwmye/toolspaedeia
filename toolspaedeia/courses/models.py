from django.contrib.auth import get_user_model
from django.db import models


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
