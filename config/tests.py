from django.test import TestCase
from blog.models import BlogPost, BlogCategory
from services.models import CaseStudy, Service


class SitemapTests(TestCase):
    def test_sitemap_returns_xml_with_static_pages(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertIn(b"<loc>https://nyrix.tech/</loc>", response.content)
        self.assertIn(b"<loc>https://nyrix.tech/it-audit</loc>", response.content)

    def test_published_blog_post_appears_in_sitemap(self):
        category = BlogCategory.objects.create(name="IT Guides", slug="it-guides")
        BlogPost.objects.create(
            title="Test Post", slug="test-post", excerpt="x", content="x", category=category, published=True
        )
        response = self.client.get("/sitemap.xml")
        self.assertIn(b"<loc>https://nyrix.tech/blog/test-post</loc>", response.content)

    def test_unpublished_blog_post_is_excluded(self):
        category = BlogCategory.objects.create(name="IT Guides", slug="it-guides")
        BlogPost.objects.create(
            title="Draft Post", slug="draft-post", excerpt="x", content="x", category=category, published=False
        )
        response = self.client.get("/sitemap.xml")
        self.assertNotIn(b"draft-post", response.content)

    def test_active_case_study_and_service_appear(self):
        Service.objects.create(name="Test Service", slug="test-service", short_description="x", description="x")
        CaseStudy.objects.create(title="Test Case", slug="test-case", summary="x", content="x")
        response = self.client.get("/sitemap.xml")
        self.assertIn(b"<loc>https://nyrix.tech/services/test-service</loc>", response.content)
        self.assertIn(b"<loc>https://nyrix.tech/case-studies/test-case</loc>", response.content)

    def test_inactive_service_and_case_study_are_excluded(self):
        Service.objects.create(
            name="Inactive Service", slug="inactive-service", short_description="x", description="x", is_active=False
        )
        CaseStudy.objects.create(title="Inactive Case", slug="inactive-case", summary="x", content="x", is_active=False)
        response = self.client.get("/sitemap.xml")
        self.assertNotIn(b"inactive-service", response.content)
        self.assertNotIn(b"inactive-case", response.content)
