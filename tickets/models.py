import uuid
from django.core.validators import FileExtensionValidator
from django.db import models
from config.validators import ALLOWED_UPLOAD_EXTENSIONS, validate_file_size


class Ticket(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        WAITING_FOR_CLIENT = "WAITING_FOR_CLIENT", "Waiting for client"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey("clients.Company", on_delete=models.CASCADE, related_name="tickets")
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="tickets_created")
    assigned_to = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="tickets_assigned"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"]), models.Index(fields=["priority"])]

    def __str__(self):
        return f"#{str(self.id)[:8]} — {self.title}"


class TicketMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="ticket_messages")
    body = models.TextField()
    attachment = models.FileField(
        upload_to="ticket_attachments/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOAD_EXTENSIONS), validate_file_size],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message on {self.ticket_id} by {self.author}"
