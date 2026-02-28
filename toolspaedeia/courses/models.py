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

        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self) -> str:
        return self.name


class Module(models.Model):
    """Model representing a module within a course."""

    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        """Meta class for the Module model."""

        ordering = ["order"]
        verbose_name = "Module"
        verbose_name_plural = "Modules"

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
        verbose_name = "Module Progression"
        verbose_name_plural = "Module Progressions"

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


class Quiz(models.Model):
    """Model representing a quiz within a module."""

    module = models.OneToOneField(Module, related_name="quiz", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    randomize_questions = models.BooleanField(default=False)
    max_questions = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        """Meta class for the Quiz model."""

        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self) -> str:
        return self.title

    def get_questions_for_attempt(self):
        """
        Return a queryset of questions for a quiz attempt, applying
        randomization and max question limits.
        """
        questions = self.questions.all()
        questions = questions.order_by("?") if self.randomize_questions else questions.order_by("order")
        if self.max_questions:
            questions = questions[: self.max_questions]
        return questions


class Question(models.Model):
    """Model representing a question within a quiz."""

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        """Meta class for the Question model."""

        ordering = ["order"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self) -> str:
        return f"{self.quiz} - {self.id} Question {self.order}"

    def get_answers(self):
        """Return a queryset of answers for this question."""
        return self.answers.all().order_by("?")


class Answer(models.Model):
    """Model representing an answer option for a quiz question."""

    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        """Meta class for the Answer model."""

        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self) -> str:
        return self.text
