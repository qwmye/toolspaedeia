import mistune
from mistune.directives import FencedDirective
from mistune.directives import TableOfContents


def markdown_to_html(markdown_text):
    """Convert MD to HTML."""
    markdown = mistune.create_markdown(
        escape=True,
        renderer="html",
        plugins=[
            "def_list",
            "task_lists",
            "superscript",
            "subscript",
            "math",
            FencedDirective([TableOfContents()]),
        ],
    )
    return markdown(markdown_text)
