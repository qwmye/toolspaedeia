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
