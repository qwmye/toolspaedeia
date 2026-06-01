import contextlib

import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.views.generic import ListView

from courses.models import Course
from purchases.models import Purchase
from toolspaedeia.mixins import TitledViewMixin

stripe.api_key = settings.STRIPE_SECRET_KEY


class PublisherIncomeView(TitledViewMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    context_object_name = "purchases"
    title = "Income"
    template_name = "purchases/publisher_income.html"
    login_url = "users:login"
    permission_required = "courses.add_course"

    def get_queryset(self):
        return (
            Purchase.objects.filter(
                state=Purchase.State.ACCEPTED,
                course__publisher=self.request.user,
            )
            .values("course_id", "course__name", "amount")
            .order_by("-amount", "course__name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = []
        total_enrollments = 0
        total_income = 0
        distinct_courses = set()

        for purchase in context["purchases"]:
            total_income += purchase["amount"]
            total_enrollments += 1
            if purchase["amount"] > 0:
                distinct_courses.add(purchase["course_id"])
                purchases.append(purchase)
                purchase["income_percentage"] = purchase["amount"] / total_income * 100

        context["purchases"] = purchases
        context["total_enrollments"] = total_enrollments
        context["total_income"] = total_income
        context["distinct_courses"] = distinct_courses
        return context


class EnrollCourseView(LoginRequiredMixin, CreateView):
    http_method_names = ["post"]
    model = Purchase
    fields = ["course"]
    login_url = "users:login"
    success_url = reverse_lazy("courses:course_browse_list")

    def form_valid(self, form):
        Purchase.objects.update_or_create(
            user=self.request.user,
            course=form.instance.course,
            defaults={
                "amount": form.instance.course.price,
                "state": Purchase.State.ACCEPTED,
                "stripe_payment_id": None,
            },
        )
        return redirect(self.request.META.get("HTTP_REFERER", self.success_url))


class CreateRefundView(LoginRequiredMixin, View):
    http_method_names = ["post"]
    login_url = "users:login"

    def post(self, request):
        course_id = request.POST.get("course_id")
        if not course_id:
            return JsonResponse({"error": "Missing course_id."}, status=400)

        purchase = Purchase.objects.get(user=request.user, course_id=course_id, state=Purchase.State.ACCEPTED)

        with contextlib.suppress(stripe.InvalidRequestError):
            stripe.Refund.create(payment_intent=purchase.stripe_payment_id)
        purchase.delete()
        return HttpResponse(status=201, headers={"HX-Redirect": reverse("courses:course_purchased_list")})


class PurchasedContentOfflineMapView(LoginRequiredMixin, View):
    http_method_names = ["get"]
    login_url = "users:login"

    def get(self, request):
        purchases = (
            Purchase.objects.filter(user=request.user, state=Purchase.State.ACCEPTED)
            .select_related("course")
            .prefetch_related("course__modules")
        )

        urls = []
        for purchase in purchases:
            course = purchase.course
            urls.append(reverse("courses:course_detail", kwargs={"course_id": course.id}))

            urls.extend(
                reverse(
                    "courses:module_detail",
                    kwargs={"course_id": course.id, "module_id": module.id},
                )
                for module in course.modules.filter(is_draft=False).order_by("order")
            )

        unique_urls = list(dict.fromkeys(urls))
        return JsonResponse({"urls": unique_urls})


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    http_method_names = ["post"]

    PAYMENT_COMPLETE_EVENTS = {"checkout.session.completed", "checkout.session.async_payment_succeeded"}
    PAYMENT_FAILED_EVENTS = {"checkout.session.async_payment_failed", "checkout.session.expired"}

    def post(self, request):
        payload = request.body
        signature = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        webhook_secret = settings.STRIPE_WEBHOOK_SECRET

        webhook_event = stripe.Webhook.construct_event(payload, signature, webhook_secret)
        course_id = webhook_event.data.object.metadata.course_id
        user_id = webhook_event.data.object.metadata.user_id
        state = None
        if webhook_event.type in self.PAYMENT_COMPLETE_EVENTS:
            state = Purchase.State.ACCEPTED
        elif webhook_event.type in self.PAYMENT_FAILED_EVENTS:
            state = Purchase.State.REFUSED

        Purchase.objects.update_or_create(
            user_id=user_id,
            course_id=course_id,
            defaults={
                "amount": webhook_event.data.object.amount_total / 100.0,
                "state": state,
                "stripe_payment_id": webhook_event.data.object.payment_intent,
            },
        )
        return HttpResponse(status=200)


class EnrollmentDialogView(LoginRequiredMixin, View):
    http_method_names = ["get"]
    login_url = "users:login"

    def get(self, request):
        course_id = request.GET.get("course_id")
        if not course_id:
            return HttpResponse("Missing course_id", status=400)

        course = get_object_or_404(Course, id=course_id, is_draft=False)

        if Purchase.objects.filter(
            user=request.user,
            course=course,
            state=Purchase.State.ACCEPTED,
        ).exists():
            return HttpResponse("Course already purchased", status=400)

        payment_link = None
        if course.price > 0:
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    customer_email=request.user.email,
                    line_items=[
                        {
                            "price_data": {
                                "currency": "eur",
                                "product_data": {"name": course.name},
                                "unit_amount": int(float(course.price) * 100),
                            },
                            "quantity": 1,
                        }
                    ],
                    mode="payment",
                    success_url=request.build_absolute_uri("/courses/purchased-courses/"),
                    cancel_url=request.build_absolute_uri("/courses/purchased-courses/"),
                    metadata={
                        "course_id": str(course.id),
                        "user_id": str(request.user.id),
                    },
                )
                payment_link = session.url
            except Exception as exc:  # noqa: BLE001
                return HttpResponse(f"Error creating payment link: {exc!s}", status=400)

        context = {
            "course": course,
            "payment_link": payment_link,
        }
        html = render_to_string("purchases/enrollment_dialog.html", context, request=request)
        return HttpResponse(html)
