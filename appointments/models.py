import uuid
from django.db import models


class Appointment(models.Model):
    class AppointmentType(models.TextChoices):
        IT_AUDIT = "IT_AUDIT", "IT Audit"
        CYBERSECURITY = "CYBERSECURITY", "Cybersecurity Consultation"
        NETWORK = "NETWORK", "Network Assessment"
        SERVER = "SERVER", "Server Assessment"
        GENERAL = "GENERAL", "General Consultation"

    class Status(models.TextChoices):
        REQUESTED = "REQUESTED", "Requested"
        CONFIRMED = "CONFIRMED", "Confirmed"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requested_by = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="appointments"
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=32, blank=True)
    company = models.CharField(max_length=200, blank=True)
    appointment_type = models.CharField(max_length=20, choices=AppointmentType.choices)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_appointment_type_display()} — {self.name}"
