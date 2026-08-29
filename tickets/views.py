from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Ticket, TicketMessage
from .serializers import TicketSerializer, TicketMessageSerializer
from notifications.services import notify_new_ticket


class TicketViewSet(viewsets.ModelViewSet):
    """
    Clients see/manage only their own company's tickets.
    Staff/admin see all tickets.
    """
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "priority"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff_role:
            return Ticket.objects.all()
        return Ticket.objects.filter(created_by=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff_role:
            # Staff may file a ticket on behalf of any company via the submitted fields.
            ticket = serializer.save(created_by=user)
        else:
            # Never trust client-submitted company/assigned_to/status — force them from
            # the requester's own profile so a client can't create a ticket under, or
            # attach one to, another company (IDOR).
            profile = getattr(user, "client_profile", None)
            if not profile:
                raise PermissionDenied("Your account isn't linked to a company yet.")
            ticket = serializer.save(
                created_by=user,
                company=profile.company,
                assigned_to=None,
                status=Ticket.Status.OPEN,
            )
        notify_new_ticket(ticket)


class TicketMessageViewSet(viewsets.ModelViewSet):
    serializer_class = TicketMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = TicketMessage.objects.all()
        if not user.is_staff_role:
            qs = qs.filter(ticket__created_by=user)
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        ticket = serializer.validated_data.get("ticket")
        if not user.is_staff_role and (ticket is None or ticket.created_by_id != user.id):
            raise PermissionDenied("You don't have access to this ticket.")
        serializer.save(author=user)
