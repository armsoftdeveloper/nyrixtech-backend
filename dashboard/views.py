from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from config.permissions import IsStaffRole
from leads.models import Lead, LeadStatus
from audits.models import ITAuditRequest
from tickets.models import Ticket
from appointments.models import Appointment
from clients.models import Company
from subscriptions.models import Subscription


class AdminDashboardView(APIView):
    """GET /api/dashboard/ — staff-only CRM-style overview."""
    permission_classes = [IsStaffRole]

    def get(self, request):
        since = timezone.now() - timedelta(days=30)
        active_subs = Subscription.objects.filter(status="ACTIVE")
        mrr = sum(s.monthly_amount for s in active_subs) if active_subs else 0

        return Response({
            "new_audit_requests": ITAuditRequest.objects.filter(status="NEW").count(),
            "new_contact_requests": Lead.objects.filter(source="contact_form", status=LeadStatus.NEW).count(),
            "total_leads": Lead.objects.count(),
            "leads_last_30_days": Lead.objects.filter(created_at__gte=since).count(),
            "active_clients": Company.objects.filter(subscriptions__status="ACTIVE").distinct().count(),
            "open_tickets": Ticket.objects.exclude(status__in=["RESOLVED", "CLOSED"]).count(),
            "upcoming_appointments": Appointment.objects.filter(
                status__in=["REQUESTED", "CONFIRMED"], preferred_date__gte=timezone.now().date()
            ).count(),
            "monthly_recurring_revenue": mrr,
            "leads_by_status": {
                choice.value: Lead.objects.filter(status=choice.value).count()
                for choice in LeadStatus
            },
        })


class ClientDashboardView(APIView):
    """GET /api/dashboard/client/ — logged-in client's own overview."""
    from rest_framework.permissions import IsAuthenticated
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, "client_profile", None)
        if not profile:
            # Not having a linked company profile yet is an expected state for a
            # self-registered account before staff link it — not an error, so this
            # returns 200 rather than 404 (which the browser logs as a request failure).
            return Response({"has_profile": False})
        company = profile.company
        return Response({
            "has_profile": True,
            "company": company.name,
            "monitoring_status": profile.monitoring_status,
            "backup_status": profile.backup_status,
            "open_tickets": Ticket.objects.filter(company=company).exclude(status__in=["RESOLVED", "CLOSED"]).count(),
            "active_subscriptions": Subscription.objects.filter(company=company, status="ACTIVE").count(),
            "upcoming_appointments": Appointment.objects.filter(
                requested_by=user, status__in=["REQUESTED", "CONFIRMED"]
            ).count(),
        })
