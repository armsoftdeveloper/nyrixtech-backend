import uuid
from django.core.validators import FileExtensionValidator
from django.db import models
from config.validators import ALLOWED_UPLOAD_EXTENSIONS, validate_file_size


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey("clients.Company", on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="uploaded_documents")
    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=[
            ("CONTRACT", "Contract"),
            ("REPORT", "Report"),
            ("INVOICE", "Invoice"),
            ("AUDIT", "Audit Report"),
            ("OTHER", "Other"),
        ],
        default="OTHER",
    )
    file = models.FileField(
        upload_to="documents/",
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOAD_EXTENSIONS), validate_file_size],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
