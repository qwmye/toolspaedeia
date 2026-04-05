import re

import mistune
from mistune.directives import FencedDirective
from mistune.directives import TableOfContents

IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "svg", "webp", "bmp", "ico"}
VIDEO_EXTENSIONS = {"mp4", "webm", "ogv"}
AUDIO_EXTENSIONS = {"mp3", "ogg", "wav", "flac", "aac"}
IFRAME_EXTENSIONS = {"pdf"}
OTHER_ALLOWED_EXTENSIONS = {"xls", "xlsx", "ods", "csv", "doc", "docx", "ppt", "pptx", "txt", "zip", "rar", "7z"}
ALLOWED_RESOURCE_EXTENSIONS = sorted(
    IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | AUDIO_EXTENSIONS | IFRAME_EXTENSIONS | OTHER_ALLOWED_EXTENSIONS
)


def resource_upload_path(instance, filename):
    """
    Store resources under resources/<publisher_username>/<filename>,
    so each publisher's uploads stay in their own directory.
    """
    publisher = instance.module.course.publisher
    return f"resources/{publisher.username}/{filename}"


def _file_extension(url):
    return url.rsplit(".", 1)[-1].lower() if "." in url else ""


def _render_resource_html(title, url):
    ext = _file_extension(url)

    if ext in IMAGE_EXTENSIONS:
        return f'<img src="{url}" alt="{title}" />'

    if ext in VIDEO_EXTENSIONS:
        return f'<video controls src="{url}" title="{title}"></video>'

    if ext in AUDIO_EXTENSIONS:
        return f'<audio controls src="{url}" title="{title}"></audio>'

    if ext in IFRAME_EXTENSIONS:
        return f'<iframe src="{url}" title="{title}" width="100%" height="600"></iframe>'

    return f'<a href="{url}">{title}</a>'


def resource_plugin(resources):
    """
    Custom plugin that renderes `resource:<title>` into embedded HTML
    (images, video, audio, PDFs) or download links, depending on the file type.
    """
    resource_map = {r.title: r.file.url for r in resources}

    titles_alt = "|".join(re.escape(t) for t in sorted(resource_map, key=len, reverse=True))
    pattern = rf"resource:(?P<resource_title>{titles_alt})"

    def parse_resource(_inline, m, state):
        title = m.group("resource_title")
        state.append_token(
            {
                "type": "resource",
                "raw": title,
                "attrs": {"url": resource_map[title]},
            }
        )
        return m.end()

    def plugin(md):
        md.inline.register("resource", pattern, parse_resource, before="link")
        if md.renderer and md.renderer.NAME == "html":
            md.renderer.register("resource", lambda _rendered, text, url: _render_resource_html(text, url))

    return plugin


def markdown_to_html(markdown_text, resources=None):
    plugins = [
        "def_list",
        "task_lists",
        "superscript",
        "subscript",
        "math",
        "strikethrough",
        "mark",
        FencedDirective([TableOfContents()]),
    ]
    if resources:
        plugins.append(resource_plugin(resources))

    markdown = mistune.create_markdown(
        escape=True,
        renderer="html",
        plugins=plugins,
    )
    return markdown(markdown_text)
