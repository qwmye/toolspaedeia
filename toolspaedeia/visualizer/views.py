from enum import Enum
from io import StringIO

import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

INCOME_TAX = 0.1


class Frecventa(Enum):
    DAILY = 365
    MONTHLY = 12
    QUARTERLY = 3
    YEARLY = 1


class Cont:
    per_annum: float
    frecventa: Frecventa

    @property
    def dobanda_reala(self):
        return self.per_annum / 100 * INCOME_TAX

    def calcul_dobanda_an(self, suma_totala: float):
        return suma_totala * (
            (1 + self.dobanda_reala/self.frecventa.value) ** self.frecventa.value
        ) - suma_totala


class ING(Cont):
    per_annum = 6
    frecventa = Frecventa.QUARTERLY


class RevolutStandard(Cont):
    per_annum = 2.5
    frecventa = Frecventa.DAILY


class RevolutMetal(Cont):
    per_annum = 3.75
    frecventa = Frecventa.DAILY


class RevolutUltra(Cont):
    per_annum = 4.25
    frecventa = Frecventa.DAILY


def generate_graph(request):
    suma_totala = 10000
    dobanzi = {
        "ING": ING().calcul_dobanda_an(suma_totala),
        "Revolut Plan Standard": RevolutStandard().calcul_dobanda_an(suma_totala),
        "Revolut Plan Metal": RevolutMetal().calcul_dobanda_an(suma_totala),
        "Revolut Plan Ultra": RevolutUltra().calcul_dobanda_an(suma_totala),
    }
    conturi, valori_dobanzi = zip(*dobanzi.items(), strict=False)

    plt.figure(figsize=(10, 10))
    plt.bar(conturi, valori_dobanzi)
    for bar_index in range(len(conturi)):
        plt.text(
            bar_index,
            valori_dobanzi[bar_index] + 1,
            f"{valori_dobanzi[bar_index]:.3f}",
            ha="center",
        )
    output_svg = StringIO()
    plt.savefig(output_svg, format="svg")
    output_svg.seek(0)
    data = output_svg.getvalue()

    return HttpResponse(data)
