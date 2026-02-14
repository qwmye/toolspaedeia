from io import StringIO

import matplotlib.pyplot as plt
import mistune


def get_svg_from_plot():
    """Generate SVG from plot."""
    output_svg = StringIO()
    plt.savefig(output_svg, format="svg")
    plt.close()
    output_svg.seek(0)
    return output_svg.getvalue()


def markdown_to_html(markdown_text):
    """Convert MD to HTML."""
    markdown = mistune.create_markdown()
    return markdown(markdown_text)
