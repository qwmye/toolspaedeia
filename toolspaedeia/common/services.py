import mistune


def markdown_to_html(markdown_text):
    """Convert MD to HTML."""
    markdown = mistune.create_markdown()
    return markdown(markdown_text)
