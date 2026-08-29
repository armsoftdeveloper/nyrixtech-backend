import uuid
from django.db import models


class LeadStatus(models.TextChoices):
    NEW = "NEW", "New"
    CONTACTED = "CONTACTED", "Contacted"
    QUALIFIED = "QUALIFIED", "Qualified"
    PROPOSAL = "PROPOSAL", "Proposal"
    NEGOTIATION = "NEGOTIATION", "Negotiation"
    WON = "WON", "Won"
    LOST = "LOST", "Lost"


class TrafficSource(models.TextChoices):
    """Marketing channel the visitor arrived from — distinct from Lead.source, which
    records which on-site form (contact_form / it_audit / appointment) created the lead."""
    DIRECT = "direct", "Direct"
    GOOGLE = "google", "Google (organic)"
    GOOGLE_ADS = "google_ads", "Google Ads"
    INSTAGRAM = "instagram", "Instagram"
    FACEBOOK = "facebook", "Facebook"
    LINKEDIN = "linkedin", "LinkedIn"
    REFERRAL = "referral", "Referral"
    OTHER = "other", "Other"


class TrafficAttributionMixin(models.Model):
    """Marketing attribution captured at submission time from the visitor's landing URL."""
    traffic_source = models.CharField(max_length=20, choices=TrafficSource.choices, default=TrafficSource.DIRECT)
    utm_source = models.CharField(max_length=150, blank=True)
    utm_medium = models.CharField(max_length=150, blank=True)
    utm_campaign = models.CharField(max_length=150, blank=True)
    utm_content = models.CharField(max_length=150, blank=True)
    utm_term = models.CharField(max_length=150, blank=True)

    class Meta:
        abstract = True


class Lead(TrafficAttributionMixin, models.Model):
    """Central CRM lead record — created from audits, contact forms, or manually by staff."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    company = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=32, blank=True)
    source = models.CharField(max_length=50, default="contact_form", help_text="contact_form, it_audit, appointment, manual")
    service_interest = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=20, choices=LeadStatus.choices, default=LeadStatus.NEW)
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_leads"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"]), models.Index(fields=["created_at"]), models.Index(fields=["traffic_source"])]

    def __str__(self):
        return f"{self.name} ({self.company or 'no company'}) — {self.status}"


class ContactRequest(TrafficAttributionMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    company = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=32, blank=True)
    service = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=LeadStatus.choices, default=LeadStatus.NEW)
    lead = models.ForeignKey(Lead, null=True, blank=True, on_delete=models.SET_NULL, related_name="contact_requests")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Contact: {self.name} — {self.email}"
