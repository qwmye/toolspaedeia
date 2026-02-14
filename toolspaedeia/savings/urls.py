from django.urls import path

from . import views

app_name = "savings"

urlpatterns = [
    path("", views.SavingsAccountList.as_view(), name="savings_accounts_list"),
    path("<pk>/", views.SavingsAccountDetailView.as_view(), name="savings_accounts_detail"),
]
