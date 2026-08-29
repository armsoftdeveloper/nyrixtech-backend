from rest_framework.test import APITestCase
from rest_framework import status
from leads.models import ContactRequest


def _payload(**overrides):
    data = {
        "name": "Jane Tester",
        "company": "Test Co",
        "email": "contact@example.com",
        "phone": "+37499000000",
        "service": "Managed IT",
        "message": "We need help with our infrastructure.",
    }
    data.update(overrides)
    return data


class ContactSubmissionTests(APITestCase):
    def test_submission_creates_contact_request_and_linked_lead(self):
        response = self.client.post("/api/contact/", _payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact = ContactRequest.objects.get(email="contact@example.com")
        self.assertIsNotNone(contact.lead)
        self.assertEqual(contact.lead.source, "contact_form")

    def test_gclid_propagates_to_lead(self):
        """The Google Ads click id must survive submission → Lead so a later CRM stage
        change (qualified, won) can be uploaded back to Google Ads as an offline conversion."""
        response = self.client.post(
            "/api/contact/",
            _payload(gclid="Cj0KCQjw_test_click_id_456"),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact = ContactRequest.objects.get(email="contact@example.com")
        self.assertEqual(contact.gclid, "Cj0KCQjw_test_click_id_456")
        self.assertEqual(contact.lead.gclid, "Cj0KCQjw_test_click_id_456")
