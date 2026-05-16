import json
from decimal import Decimal
from json import JSONDecodeError

import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.db.models import Sum
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
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
            .values("course_id", "course__name")
            .annotate(
                sales_count=Count("id"),
                total_income=Sum("amount"),
                income_percentage=Sum("amount") / Sum("course__price") * 100,
            )
            .order_by("-total_income", "course__name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = list(context["purchases"])
        total_sales = sum(row["sales_count"] for row in purchases)
        total_income = sum((row["total_income"] for row in purchases), start=Decimal("0.00"))
        context["purchases"] = purchases
        context["total_sales"] = total_sales
        context["total_income"] = total_income
        return context


class PurchaseCourseView(LoginRequiredMixin, CreateView):
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
                "stripe_checkout_session_id": None,
            },
        )
        return redirect(self.request.META.get("HTTP_REFERER", self.success_url))


class CreateCheckoutSessionView(LoginRequiredMixin, View):
    http_method_names = ["post"]
    login_url = "users:login"

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
        except JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)

        course_id = data.get("course_id")
        if not course_id:
            return JsonResponse({"error": "Missing course_id."}, status=400)

        course = get_object_or_404(Course, id=course_id, is_draft=False)

        if Purchase.objects.filter(
            user=request.user,
            course=course,
            state=Purchase.State.ACCEPTED,
        ).exists():
            return JsonResponse({"error": "Course already purchased."}, status=400)

        amount = int(float(course.price) * 100)

        purchase, _ = Purchase.objects.update_or_create(
            user=request.user,
            course=course,
            defaults={
                "amount": course.price,
                "state": Purchase.State.PENDING,
                "stripe_checkout_session_id": None,
            },
        )

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                customer_email=request.user.email,
                line_items=[
                    {
                        "price_data": {
                            "currency": "eur",
                            "product_data": {"name": course.name},
                            "unit_amount": amount,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=request.build_absolute_uri("/courses/browse/?success"),
                cancel_url=request.build_absolute_uri("/courses/browse/?canceled"),
                metadata={
                    "purchase_id": str(purchase.id),
                    "course_id": str(course.id),
                    "user_id": str(request.user.id),
                },
            )
        except Exception as exc:  # noqa: BLE001
            return JsonResponse({"error": str(exc)}, status=400)

        purchase.stripe_checkout_session_id = session.id
        purchase.save(update_fields=["stripe_checkout_session_id"])
        return JsonResponse({"id": session.id})


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    http_method_names = ["post"]

    @staticmethod
    def _get_purchase_from_session(session_data):
        session_id = session_data.get("id")
        if session_id:
            purchase = Purchase.objects.filter(stripe_checkout_session_id=session_id).first()
            if purchase:
                return purchase

        metadata = session_data.get("metadata") or {}
        purchase_id = metadata.get("purchase_id")
        if purchase_id:
            return Purchase.objects.filter(id=purchase_id).first()
        return None

    def post(self, request):
        payload = request.body
        signature = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        webhook_secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")

        try:
            if webhook_secret:
                event = stripe.Webhook.construct_event(payload, signature, webhook_secret)
            else:
                event = json.loads(payload.decode("utf-8"))
        except Exception:  # noqa: BLE001
            return HttpResponse(status=400)

        event_type = event.get("type")
        session_data = (event.get("data") or {}).get("object") or {}
        purchase = self._get_purchase_from_session(session_data)

        if purchase:
            if event_type == "checkout.session.completed":
                purchase.state = Purchase.State.ACCEPTED
                purchase.save(update_fields=["state"])
            elif event_type in {"checkout.session.async_payment_failed", "checkout.session.expired"}:
                if purchase.state != Purchase.State.ACCEPTED:
                    purchase.state = Purchase.State.REFUSED
                    purchase.save(update_fields=["state"])

        return HttpResponse(status=200)
