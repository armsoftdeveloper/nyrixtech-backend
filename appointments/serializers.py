from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id", "name", "email", "phone", "company", "appointment_type",
            "preferred_date", "preferred_time", "notes", "status", "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]
