from django.contrib import admin

from .models import SavingsAccount


# Register your models here.
@admin.register(SavingsAccount)
class SavingsAccountAdmin(admin.ModelAdmin):
    pass
