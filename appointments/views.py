from rest_framework import viewsets, permissions
from config.permissions import IsStaffRole
from .models import Appointment
from .serializers import AppointmentSerializer
from notifications.services import notify_new_appointment


class AppointmentViewSet(viewsets.ModelViewSet):
    """POST is public (booking a consultation). Listing/managing is staff-only,
    except a logged-in client can see their own appointments."""
    serializer_class = AppointmentSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Appointment.objects.none()
        if user.is_staff_role:
            return Appointment.objects.all()
        return Appointment.objects.filter(requested_by=user)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        appointment = serializer.save(requested_by=user)
        notify_new_appointment(appointment)
