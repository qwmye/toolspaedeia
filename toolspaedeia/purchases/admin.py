from django.contrib import admin

from purchases.models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "course", "amount", "state", "stripe_payment_id", "purchase_date"]
    list_filter = ["state", "purchase_date"]
    search_fields = ["user__username", "course__name", "stripe_payment_id"]
