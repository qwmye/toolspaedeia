from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models import Q
from django.views.generic import TemplateView

from courses.models import Course
from courses.models import CourseTag
from courses.models import ModuleProgression
from purchases.models import Purchase
from toolspaedeia.mixins import TitledViewMixin


class HomeView(TitledViewMixin, TemplateView):
    template_name = "home.html"
    title = "Home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course_count = Course.objects.count()
        courses_over_k = course_count // 5 * 5

        accepted_purchases = Purchase.objects.filter(state=Purchase.State.ACCEPTED).select_related("course", "user")
        enrollments_count = accepted_purchases.count()

        publisher_ids = Course.objects.exclude(publisher__isnull=True).values_list("publisher_id", flat=True).distinct()
        publishers_count = len(publisher_ids)

        enrolled_students_count = get_user_model().objects.count()

        completion_rate = 0
        for enrollment in accepted_purchases:
            total_modules = enrollment.course.modules.filter(is_draft=False).count()
            if total_modules == 0:
                continue
            completed_modules = ModuleProgression.objects.filter(
                user=enrollment.user,
                module__course=enrollment.course,
                module__is_draft=False,
                completed=True,
            ).count()
            completion_rate += completed_modules / total_modules

        completion_rate = (completion_rate / enrollments_count) * 100 if enrollments_count else 0

        top_categories = list(
            CourseTag.objects.annotate(
                enrolled_students=Count(
                    "courses__purchases",
                    filter=Q(courses__purchases__state=Purchase.State.ACCEPTED),
                    distinct=True,
                ),
            )
            .filter(enrolled_students__gt=0)
            .order_by("-enrolled_students", "name")[:5]
        )

        context.update(
            {
                "courses_over_k": courses_over_k,
                "enrollments_count": enrollments_count,
                "enrolled_students_count": enrolled_students_count,
                "publishers_count": publishers_count,
                "completion_rate": completion_rate,
                "top_categories": top_categories,
            }
        )
        return context
