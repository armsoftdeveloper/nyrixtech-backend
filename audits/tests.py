from rest_framework.test import APITestCase
from rest_framework import status
from audits.models import ITAuditRequest
from leads.models import Lead


def _payload(**overrides):
    data = {
        "company_name": "Test Co",
        "contact_person": "Jane Tester",
        "email": "audit@example.com",
        "phone": "+37499000000",
        "employee_count": "6-20",
        "infrastructure": [],
        "problems": [],
        "problems_other": "",
        "preferred_contact_method": "EMAIL",
    }
    data.update(overrides)
    return data


class ITAuditSubmissionTests(APITestCase):
    def test_submission_creates_audit_and_linked_lead(self):
        response = self.client.post("/api/audits/", _payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        audit = ITAuditRequest.objects.get(email="audit@example.com")
        self.assertIsNotNone(audit.lead)
        self.assertEqual(audit.lead.source, "it_audit")

    def test_utm_and_traffic_source_propagate_to_lead(self):
        response = self.client.post(
            "/api/audits/",
            _payload(
                traffic_source="google_ads",
                utm_source="google",
                utm_medium="cpc",
                utm_campaign="spring_launch",
                utm_content="ad1",
                utm_term="managed it armenia",
            ),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        audit = ITAuditRequest.objects.get(email="audit@example.com")
        self.assertEqual(audit.traffic_source, "google_ads")
        self.assertEqual(audit.lead.traffic_source, "google_ads")
        self.assertEqual(audit.lead.utm_campaign, "spring_launch")

    def test_duplicate_submission_within_window_does_not_create_second_lead(self):
        first = self.client.post("/api/audits/", _payload(), format="json")
        second = self.client.post("/api/audits/", _payload(contact_person="Jane Again"), format="json")

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_201_CREATED)
        self.assertEqual(first.data["id"], second.data["id"])
        self.assertEqual(ITAuditRequest.objects.filter(email="audit@example.com").count(), 1)
        self.assertEqual(Lead.objects.filter(email="audit@example.com").count(), 1)

    def test_different_email_is_not_treated_as_duplicate(self):
        self.client.post("/api/audits/", _payload(), format="json")
        response = self.client.post("/api/audits/", _payload(email="other@example.com"), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ITAuditRequest.objects.count(), 2)
