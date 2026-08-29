import uuid
from django.db import models
from leads.models import TrafficAttributionMixin


class ITAuditRequest(TrafficAttributionMixin, models.Model):
    """The Free IT Audit multi-step form submission — the site's primary conversion goal."""

    class ContactMethod(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        PHONE = "PHONE", "Phone"
        WHATSAPP = "WHATSAPP", "WhatsApp"

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        SCHEDULED = "SCHEDULED", "Scheduled"
        COMPLETED = "COMPLETED", "Completed"
        CONVERTED = "CONVERTED", "Converted to client"
        DISMISSED = "DISMISSED", "Dismissed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Step 1
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=32)

    # Step 2
    employee_count = models.CharField(
        max_length=20,
        choices=[
            ("1-5", "1–5"),
            ("6-20", "6–20"),
            ("21-50", "21–50"),
            ("51-200", "51–200"),
            ("200+", "200+"),
        ],
    )

    # Step 3 — infrastructure (multi-select)
    infrastructure = models.JSONField(
        default=list,
        blank=True,
        help_text="Windows, Linux, Cloud, On-premise servers, MikroTik, FortiGate, Cisco, Wi-Fi, CCTV, VPN, Backup, Monitoring",
    )

    # Step 4 — problems (multi-select)
    problems = models.JSONField(
        default=list,
        blank=True,
        help_text="Network, Security, Servers, Backup, Performance, Support, Other",
    )
    problems_other = models.CharField(max_length=300, blank=True)

    # Step 5
    preferred_contact_method = models.CharField(
        max_length=10, choices=ContactMethod.choices, default=ContactMethod.EMAIL
    )

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    internal_notes = models.TextField(blank=True)
    lead = models.ForeignKey(
        "leads.Lead", null=True, blank=True, on_delete=models.SET_NULL, related_name="audit_requests"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"]), models.Index(fields=["created_at"])]

    def __str__(self):
        return f"IT Audit: {self.company_name} ({self.status})"
