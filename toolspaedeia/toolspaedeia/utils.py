from io import StringIO

import matplotlib.pyplot as plt


def get_svg_from_plot():
    output_svg = StringIO()
    plt.savefig(output_svg, format="svg")
    output_svg.seek(0)
    return output_svg.getvalue()
