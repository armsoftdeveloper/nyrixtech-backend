"""Shared upload validators used across apps that accept file uploads (documents, ticket attachments)."""
from django.core.exceptions import ValidationError

MAX_UPLOAD_SIZE_MB = 20

ALLOWED_UPLOAD_EXTENSIONS = [
    "pdf", "doc", "docx", "xls", "xlsx", "csv", "txt",
    "png", "jpg", "jpeg",
]


def validate_file_size(file):
    limit = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file.size > limit:
        raise ValidationError(f"File too large. Maximum upload size is {MAX_UPLOAD_SIZE_MB}MB.")
