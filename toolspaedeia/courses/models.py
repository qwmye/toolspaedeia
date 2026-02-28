from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Course(models.Model):
    """
    The course is the primary "content" entity in the Paedeia system.
    Modules are written for a course, users can buy and enroll in a course,
    and it is the main attraction for users, through a complex and efficient
    browser.

    TODO: in the future, it is planned to add ratings and comments for courses.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    publisher = models.ForeignKey(
        get_user_model(), related_name="published_courses", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        """Ensure correctness of verbose names."""

        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self) -> str:
        return self.name


class Module(models.Model):
    """
    Each course is made up of one or more modules, which are the main content
    sections of the course.
    """

    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        """
        Add default ordering for modules, instead of relying on the creation
        order. Ensure correctness of verbose names.
        """

        ordering = ["order"]
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    def __str__(self) -> str:
        return self.title


class ModuleProgression(models.Model):
    """
    Keep track of the progression of a user throughout the course, by marking
    each module when it is completed.
    """

    user = models.ForeignKey(get_user_model(), related_name="module_progressions", on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name="progressions", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        """
        Module progression is unique for user + module combination. A user
        cannot have the same module in progress multiple times at the same time,
        even with different completion rates.
        Also, ensure correctness of verbose names.
        """

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
    """
    Modules can each (optionally) have a quiz.

    The text of the quiz will be rendered the same way as the module content,
    so it can include markdown, images, formulas, etc.
    """

    module = models.OneToOneField(Module, related_name="quiz", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    randomize_questions = models.BooleanField(default=False)
    max_questions = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        """Ensure correctness of verbose names."""

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
    """
    Each quiz can have one or more questions.

    The text of the question will be rendered the same way as the module content
    and it can include special text, markdown, images, formulas, etc.
    Questions offer a fallback ordering, in case randomization is not enabled
    for the entire quiz, instead of relying on the creation order.
    """

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        """
        Add ordering by the question order field, and ensure the correctness of
        the verbose names.
        """

        ordering = ["order"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self) -> str:
        return f"{self.quiz} - {self.id} Question {self.order}"

    def get_answers(self):
        """Return the randomized answers of the question."""
        return self.answers.order_by("?")


class Answer(models.Model):
    """
    Each question has one or more possible answers. Each answer can be marked as
    correct, ensuring the possibility of logic for multiple answers being
    correct at the same time, or even no correct answers.

    Unlike with the questions, the text is not markdown. It will be
    rendered as plain text. The text has a max length, so that fitting on a
    single line is not compromised and the UI is not broken.
    """

    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        """Ensure correctness of verbose names."""

        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self) -> str:
        return self.text
