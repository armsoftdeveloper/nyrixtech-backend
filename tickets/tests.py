from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from clients.models import Company, ClientProfile
from tickets.models import Ticket

User = get_user_model()


class TicketIdorTests(APITestCase):
    def setUp(self):
        self.own_company = Company.objects.create(name="Own Co")
        self.other_company = Company.objects.create(name="Other Co")

        self.client_user = User.objects.create_user(username="clientuser", password="Xk9#mQ2vLp7z")
        ClientProfile.objects.create(user=self.client_user, company=self.own_company)

        self.other_user = User.objects.create_user(username="otheruser", password="Xk9#mQ2vLp7z")
        ClientProfile.objects.create(user=self.other_user, company=self.other_company)

        self.client.force_authenticate(user=self.client_user)

    def test_client_cannot_create_ticket_under_another_company(self):
        response = self.client.post(
            "/api/tickets/",
            {"company": str(self.other_company.id), "title": "Test", "description": "desc"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ticket = Ticket.objects.get(id=response.data["id"])
        # The submitted (other) company must be ignored — forced to the requester's own company.
        self.assertEqual(ticket.company_id, self.own_company.id)

    def test_client_without_profile_cannot_create_ticket(self):
        orphan = User.objects.create_user(username="orphanuser", password="Xk9#mQ2vLp7z")
        self.client.force_authenticate(user=orphan)
        response = self.client.post(
            "/api/tickets/",
            {"company": str(self.own_company.id), "title": "Test", "description": "desc"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_cannot_message_another_users_ticket(self):
        other_ticket = Ticket.objects.create(company=self.other_company, created_by=self.other_user, title="T", description="d")
        response = self.client.post("/api/tickets/messages/", {"ticket": str(other_ticket.id), "body": "hi"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
