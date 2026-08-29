from django.contrib import admin
from .models import Ticket, TicketMessage


class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "priority", "status", "created_by", "assigned_to", "created_at")
    list_filter = ("status", "priority")
    inlines = [TicketMessageInline]
