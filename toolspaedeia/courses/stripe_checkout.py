import json

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from courses.models import Course
from users.models import Purchase

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
@require_POST
def create_checkout_session(request):
    data = json.loads(request.body)
    course_id = data.get("course_id")
    course = get_object_or_404(Course, id=course_id)
    # Stripe expects amount in cents
    amount = int(float(course.price) * 100)
    try:
        user_email = request.user.email if request.user.is_authenticated else None
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=user_email,
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": course.name,
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri("/courses/browse/?success"),
            cancel_url=request.build_absolute_uri("/courses/browse/?canceled"),
            metadata={"course_id": course.id},
        )
        Purchase.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
        )
        return JsonResponse({"id": session.id})
    except Exception as e:  # noqa: BLE001
        return JsonResponse({"error": str(e)}, status=400)
