from rest_framework import viewsets, permissions
from config.permissions import IsStaffRole
from .models import Lead, ContactRequest, LeadStatus
from .serializers import LeadSerializer, ContactRequestSerializer
from notifications.services import notify_new_contact_request


class ContactRequestViewSet(viewsets.ModelViewSet):
    """POST /api/contact/ -> public. GET/PATCH -> staff only."""
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [IsStaffRole()]

    def perform_create(self, serializer):
        contact = serializer.save()
        lead = Lead.objects.create(
            name=contact.name,
            company=contact.company,
            email=contact.email,
            phone=contact.phone,
            source="contact_form",
            service_interest=contact.service,
            status=LeadStatus.NEW,
            traffic_source=contact.traffic_source,
            utm_source=contact.utm_source,
            utm_medium=contact.utm_medium,
            utm_campaign=contact.utm_campaign,
            utm_content=contact.utm_content,
            utm_term=contact.utm_term,
        )
        contact.lead = lead
        contact.save(update_fields=["lead"])
        notify_new_contact_request(contact)


class LeadViewSet(viewsets.ModelViewSet):
    """Staff-only CRM lead management."""
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsStaffRole]
    filterset_fields = ["status", "source", "traffic_source"]
