import matplotlib.pyplot as plt
from django.views.generic import DetailView
from django.views.generic import ListView

from toolspaedeia.utils import get_svg_from_plot

from .models import SavingsAccount


class SavingsAccountList(ListView):
    """List all savings accounts."""

    model = SavingsAccount


class SavingsAccountDetailView(DetailView):
    """
    Details of a saving account.

    Shows a projection of the balance over time.
    """

    model = SavingsAccount

    def get_context_data(self, *args, **kwargs):
        """Add projection data to the context."""
        context_data = super().get_context_data(*args, **kwargs)

        years = 10
        balance = 10000

        context_data["initial_balance"] = balance
        context_data["years"] = years

        plt.figure(figsize=(years, years))
        yearly_income = []
        for _ in range(1, years + 1):
            yearly_income.append(self.get_object().annual_income(balance))
            balance += yearly_income[-1]
        plt.plot(range(1, len(yearly_income) + 1), yearly_income, "b-o")
        for x, y in enumerate(yearly_income):
            plt.text(x + 0.01 * abs(plt.axis()[1] - plt.axis()[0]), y, f"{y:.5f}")
        plt.title(f"{years} Year Projection")

        context_data["projection"] = get_svg_from_plot()
        context_data["final_balance"] = balance
        context_data["balance_diff"] = context_data["final_balance"] - context_data["initial_balance"]

        return context_data
