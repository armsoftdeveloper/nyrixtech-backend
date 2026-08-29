from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from clients.models import Company, ClientProfile
from documents.models import Document

User = get_user_model()


class DocumentUploadValidationTests(APITestCase):
    def setUp(self):
        self.own_company = Company.objects.create(name="Own Co")
        self.other_company = Company.objects.create(name="Other Co")
        self.client_user = User.objects.create_user(username="docclient", password="Xk9#mQ2vLp7z")
        ClientProfile.objects.create(user=self.client_user, company=self.own_company)
        self.client.force_authenticate(user=self.client_user)

    def test_disallowed_extension_is_rejected(self):
        bad_file = SimpleUploadedFile("malware.exe", b"MZ fake", content_type="application/octet-stream")
        response = self.client.post(
            "/api/documents/",
            {"company": str(self.own_company.id), "title": "Test", "category": "OTHER", "file": bad_file},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_allowed_extension_is_accepted(self):
        good_file = SimpleUploadedFile("report.pdf", b"%PDF-1.4 fake", content_type="application/pdf")
        response = self.client.post(
            "/api/documents/",
            {"company": str(self.own_company.id), "title": "Test", "category": "OTHER", "file": good_file},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_cannot_attach_document_to_another_company(self):
        good_file = SimpleUploadedFile("report.pdf", b"%PDF-1.4 fake", content_type="application/pdf")
        response = self.client.post(
            "/api/documents/",
            {"company": str(self.other_company.id), "title": "Test", "category": "OTHER", "file": good_file},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        doc = Document.objects.get(id=response.data["id"])
        self.assertEqual(doc.company_id, self.own_company.id)
