from rest_framework import serializers
from .models import Ticket, TicketMessage


class TicketMessageSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = TicketMessage
        fields = ["id", "ticket", "author", "author_name", "body", "attachment", "created_at"]
        read_only_fields = ["id", "author", "created_at"]


class TicketSerializer(serializers.ModelSerializer):
    messages = TicketMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id", "company", "created_by", "assigned_to", "title", "description",
            "category", "priority", "status", "messages", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
