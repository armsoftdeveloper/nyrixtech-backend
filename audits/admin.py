from django.contrib import admin
from .models import ITAuditRequest


@admin.register(ITAuditRequest)
class ITAuditRequestAdmin(admin.ModelAdmin):
    list_display = ("company_name", "contact_person", "email", "employee_count", "traffic_source", "status", "created_at")
    list_filter = ("status", "employee_count", "traffic_source")
    search_fields = ("company_name", "contact_person", "email", "utm_campaign")
    list_editable = ("status",)
