from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, permissions
from config.permissions import IsStaffRole
from .models import ITAuditRequest
from .serializers import ITAuditRequestSerializer, ITAuditRequestAdminSerializer
from notifications.services import notify_new_audit_request
from leads.models import Lead, LeadStatus

# Prevents double-clicks / accidental resubmits from creating duplicate CRM leads and
# duplicate notification emails for the same company within a short window.
DUPLICATE_WINDOW_MINUTES = 10


class ITAuditRequestViewSet(viewsets.ModelViewSet):
    """
    POST /api/audits/  -> public, creates a Free IT Audit request (and a CRM Lead)
    GET  /api/audits/  -> staff only, list all requests
    PATCH /api/audits/:id/ -> staff only, update status/notes
    """
    queryset = ITAuditRequest.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve", "partial_update", "update"):
            return ITAuditRequestAdminSerializer
        return ITAuditRequestSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [IsStaffRole()]

    def perform_create(self, serializer):
        email = serializer.validated_data.get("email", "")
        company_name = serializer.validated_data.get("company_name", "")
        recent_cutoff = timezone.now() - timedelta(minutes=DUPLICATE_WINDOW_MINUTES)
        duplicate = (
            ITAuditRequest.objects.filter(
                email__iexact=email, company_name__iexact=company_name, created_at__gte=recent_cutoff
            )
            .order_by("-created_at")
            .first()
        )
        if duplicate:
            # Same company + email resubmitted within the window (double-click, retry after
            # a flaky connection, etc). Return the existing request instead of creating a
            # second lead and sending a second notification email.
            serializer.instance = duplicate
            return

        audit = serializer.save()
        lead = Lead.objects.create(
            name=audit.contact_person,
            company=audit.company_name,
            email=audit.email,
            phone=audit.phone,
            source="it_audit",
            service_interest="Free IT Audit",
            status=LeadStatus.NEW,
            traffic_source=audit.traffic_source,
            utm_source=audit.utm_source,
            utm_medium=audit.utm_medium,
            utm_campaign=audit.utm_campaign,
            utm_content=audit.utm_content,
            utm_term=audit.utm_term,
            gclid=audit.gclid,
        )
        audit.lead = lead
        audit.save(update_fields=["lead"])
        notify_new_audit_request(audit)
