from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "appointment_type", "preferred_date", "status", "created_at")
    list_filter = ("appointment_type", "status")
    list_editable = ("status",)
