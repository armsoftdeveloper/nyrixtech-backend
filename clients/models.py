import uuid
from django.db import models


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=120, blank=True)
    employee_count = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ClientProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="client_profile")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="client_profiles")
    job_title = models.CharField(max_length=150, blank=True)
    is_primary_contact = models.BooleanField(default=False)
    monitoring_status = models.CharField(
        max_length=20,
        choices=[("HEALTHY", "Healthy"), ("WARNING", "Warning"), ("CRITICAL", "Critical"), ("UNKNOWN", "Unknown")],
        default="UNKNOWN",
        help_text="Demo/mock value until real monitoring integration (e.g. Zabbix) is connected",
    )
    backup_status = models.CharField(
        max_length=20,
        choices=[("OK", "OK"), ("STALE", "Stale"), ("FAILED", "Failed"), ("UNKNOWN", "Unknown")],
        default="UNKNOWN",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} @ {self.company.name}"
