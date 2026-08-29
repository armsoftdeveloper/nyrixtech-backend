import uuid
from django.db import models


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} → {self.user}"
