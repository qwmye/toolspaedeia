from django.db import models


class Course(models.Model):
    """Model representing a course in the Paedeia system."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self) -> str:
        return self.name


class Module(models.Model):
    """Model representing a module within a course."""

    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self) -> str:
        return self.title
