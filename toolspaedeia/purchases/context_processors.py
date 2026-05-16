from django.conf import settings


def stripe_keys(_request):
    return {
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
    }
