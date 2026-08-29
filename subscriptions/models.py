import uuid
from django.db import models


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey("clients.Company", on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey("services.ServicePlan", on_delete=models.PROTECT, related_name="subscriptions")
    status = models.CharField(
        max_length=20,
        choices=[("ACTIVE", "Active"), ("PAUSED", "Paused"), ("CANCELLED", "Cancelled")],
        default="ACTIVE",
    )
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, default="AMD")
    start_date = models.DateField()
    renewal_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} — {self.plan.name}"


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="invoices")
    number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, default="AMD")
    status = models.CharField(
        max_length=20,
        choices=[("DRAFT", "Draft"), ("SENT", "Sent"), ("PAID", "Paid"), ("OVERDUE", "Overdue")],
        default="DRAFT",
    )
    issue_date = models.DateField()
    due_date = models.DateField()
    pdf_file = models.FileField(upload_to="invoices/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number
