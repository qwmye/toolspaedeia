from enum import Enum

import matplotlib.pyplot as plt
from django import forms
from django.http import HttpResponse
from django.views.generic import FormView

from toolspaedeia.utils import get_svg_from_plot


class Frecventa(Enum):
    """Possible frequencies for interest calculation."""

    DAILY = 365
    MONTHLY = 12
    QUARTERLY = 3
    YEARLY = 1


class Cont:
    """Cont de economii."""

    per_annum: float
    frecventa: Frecventa
    income_tax: float = 0.1

    @property
    def dobanda_reala(self):
        """Interest after tax."""
        return self.per_annum / 100 * self.income_tax

    def calcul_dobanda_an(self, suma_totala: float):
        """Compute the interest of the account."""
        return suma_totala * ((1 + self.dobanda_reala / self.frecventa.value) ** self.frecventa.value) - suma_totala


class ING(Cont):
    """ING economy account."""

    per_annum = 6
    frecventa = Frecventa.QUARTERLY


class RevolutStandard(Cont):
    """Revolut economy account, "Standard" plan."""

    per_annum = 2.5
    frecventa = Frecventa.DAILY


class RevolutMetal(Cont):
    """Revolut economy account, "Metal" plan."""

    per_annum = 3.75
    frecventa = Frecventa.DAILY


class RevolutUltra(Cont):
    """Revolut economy account, "Ultra" plan."""

    per_annum = 4.25
    frecventa = Frecventa.DAILY


class Salt(Cont):
    """Salt economy account Bank."""

    per_annum = 6.75
    frecventa = Frecventa.YEARLY


class BT(Cont):
    """BT economy account."""

    per_annum = 6.25
    frecventa = Frecventa.YEARLY


def get_demo_svg(*, initial_balance: float | None = None):
    """Functie generica pentru a genera SVG-ul demo."""
    initial_balance = float(initial_balance or 1e5)
    dobanzi = {
        "ING": ING().calcul_dobanda_an(initial_balance),
        "Revolut Standard": RevolutStandard().calcul_dobanda_an(initial_balance),
        "Revolut Metal": RevolutMetal().calcul_dobanda_an(initial_balance),
        "Revolut Ultra": RevolutUltra().calcul_dobanda_an(initial_balance),
        "Salt Bank": Salt().calcul_dobanda_an(initial_balance),
        "BT": BT().calcul_dobanda_an(initial_balance),
    }
    conturi, valori_dobanzi = zip(*dobanzi.items(), strict=False)

    plt.figure(figsize=(2 * len(dobanzi), 2 * len(dobanzi)))
    plt.bar(conturi, valori_dobanzi)
    for bar_index in range(len(conturi)):
        plt.text(
            bar_index,
            valori_dobanzi[bar_index] + 0.01 * abs(plt.axis()[-1] - plt.axis()[-2]),
            f"{valori_dobanzi[bar_index]:.3f}",
            ha="center",
        )
    return get_svg_from_plot()


class VisualizerForm(forms.Form):
    """Form for the visualizer."""

    initial_balance = forms.FloatField(min_value=0, initial=10000, required=False)


class VisualizerView(FormView):
    """Visualize the projection of the balance over time."""

    template_name = "visualizer/visualizer.html"
    form_class = VisualizerForm

    def get_context_data(self, **kwargs):
        """Add the projection SVG to the context."""
        context_data = super().get_context_data(**kwargs)

        form = kwargs.get("form") or self.get_form()
        initial_balance = form.data.get("initial_balance") or form.initial.get("initial_balance")
        context_data["projection"] = get_demo_svg(initial_balance=initial_balance)

        return context_data

    def form_valid(self, form: forms.Form):
        """
        Return the projection SVG if the request is AJAX.
        Render the visualizer page otherwise.
        """
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            initial_balance = form.data.get("initial_balance")
            return HttpResponse(get_demo_svg(initial_balance=initial_balance))
        return self.render_to_response(self.get_context_data(form=form))
