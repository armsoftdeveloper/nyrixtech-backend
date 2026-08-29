import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        CLIENT = "CLIENT", "Client"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    phone = models.CharField(max_length=32, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    @property
    def is_staff_role(self):
        return self.role in (self.Role.ADMIN, self.Role.STAFF)
