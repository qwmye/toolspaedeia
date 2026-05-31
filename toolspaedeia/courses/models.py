from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from courses.markdown import ALLOWED_RESOURCE_EXTENSIONS
from courses.markdown import resource_upload_path


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("0.00"))
    publisher = models.ForeignKey(
        get_user_model(), related_name="published_courses", on_delete=models.SET_NULL, null=True
    )

    is_draft = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self) -> str:
        return self.name


class CourseTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    courses = models.ManyToManyField(Course, related_name="tags", blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Course Tag"
        verbose_name_plural = "Course Tags"

    def __str__(self) -> str:
        return self.name

    def clean(self):
        super().clean()
        self.name = (self.name or "").strip().lower()

        if not self.name:
            raise ValidationError({"name": "Tag name cannot be empty."})

        if len(self.name.split()) != 1:
            raise ValidationError({"name": "Tag name must be a single word."})

        if not self.name.isalnum():
            raise ValidationError({"name": "Tag name must contain only lowercase letters and numbers."})


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    order = models.PositiveIntegerField()

    is_draft = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    def __str__(self) -> str:
        return self.title


class ModuleProgression(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="module_progressions", on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name="progressions", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "module")
        verbose_name = "Module Progression"
        verbose_name_plural = "Module Progressions"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.module.title} - {'Completed' if self.completed else 'In Progress'}"

    def mark_completed(self):
        self.completed = True
        self.completion_date = timezone.now()
        self.save()

    def mark_in_progress(self):
        self.completed = False
        self.completion_date = None
        self.save()


class Quiz(models.Model):
    module = models.OneToOneField(Module, related_name="quiz", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    randomize_questions = models.BooleanField(default=False)
    track_attempts = models.BooleanField(default=True)
    max_questions = models.PositiveIntegerField(null=True, blank=True)
    max_attempts = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self) -> str:
        return self.title

    def clean(self):
        super().clean()
        if self.track_attempts and not self.max_attempts:
            raise ValidationError(
                {"max_attempts": "Max attempts must be greater than 0 when attempt tracking is enabled."}
            )

    def get_questions_for_attempt(self):
        questions = self.questions.all()
        questions = questions.order_by("?") if self.randomize_questions else questions.order_by("order")
        if self.max_questions:
            questions = questions[: self.max_questions]
        return questions


class QuizAttempt(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="quiz_attempts", on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name="attempts", on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.quiz.title} - Attempt on {self.completion_date}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self) -> str:
        return f"{self.quiz} - {self.id} Question {self.order}"

    def get_answers(self):
        return self.answers.order_by("?")


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self) -> str:
        return self.text


class Resource(models.Model):
    module = models.ForeignKey(Module, related_name="resources", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to=resource_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_RESOURCE_EXTENSIONS)],
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title
