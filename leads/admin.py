from django.contrib import admin
from .models import Lead, ContactRequest


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "source", "traffic_source", "status", "assigned_to", "created_at")
    list_filter = ("status", "source", "traffic_source")
    search_fields = ("name", "company", "email", "utm_campaign")
    list_editable = ("status",)


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "service", "traffic_source", "status", "created_at")
    list_filter = ("status", "traffic_source")
    search_fields = ("name", "email", "utm_campaign")
