"""
Dynamic sitemap.xml, served by the backend so it reflects the current published content
(blog posts, case studies, services) with no manual regeneration step. In production, nginx
proxies GET /sitemap.xml to this backend alongside /api/, /admin/, /static/ and /media/ — see
nginx/nginx.conf. The frontend's static robots.txt already points to this URL.

Kept deliberately simple (no django.contrib.sites / django.contrib.sitemaps): those pull in
a whole app + a Site DB row to manage just to resolve a domain name we already know via
SITE_URL, for a sitemap with four small querysets. A plain view is less machinery, not more.
"""
from django.conf import settings
from django.http import HttpResponse
from blog.models import BlogPost
from services.models import CaseStudy, Service

# (path, priority, changefreq) for pages that aren't backed by a database model.
STATIC_PAGES = [
    ("/", "1.0", "weekly"),
    ("/it-audit", "0.9", "monthly"),
    ("/services", "0.9", "monthly"),
    ("/solutions", "0.7", "monthly"),
    ("/industries", "0.7", "monthly"),
    ("/pricing", "0.8", "monthly"),
    ("/about", "0.6", "monthly"),
    ("/contact", "0.7", "monthly"),
    ("/faq", "0.6", "monthly"),
    ("/case-studies", "0.6", "monthly"),
    ("/blog", "0.7", "weekly"),
    ("/privacy-policy", "0.2", "yearly"),
    ("/terms", "0.2", "yearly"),
    ("/cookie-policy", "0.2", "yearly"),
]


def _entry(path, priority=None, changefreq=None, lastmod=None):
    parts = [f"  <url>\n    <loc>{settings.SITE_URL}{path}</loc>\n"]
    if lastmod is not None:
        parts.append(f"    <lastmod>{lastmod.date().isoformat()}</lastmod>\n")
    if changefreq:
        parts.append(f"    <changefreq>{changefreq}</changefreq>\n")
    if priority:
        parts.append(f"    <priority>{priority}</priority>\n")
    parts.append("  </url>\n")
    return "".join(parts)


def sitemap_xml(request):
    entries = [_entry(path, priority, changefreq) for path, priority, changefreq in STATIC_PAGES]

    for service in Service.objects.filter(is_active=True):
        entries.append(_entry(f"/services/{service.slug}", "0.8", "monthly", lastmod=service.updated_at))

    for post in BlogPost.objects.filter(published=True):
        entries.append(_entry(f"/blog/{post.slug}", "0.5", "yearly", lastmod=post.updated_at))

    for case_study in CaseStudy.objects.filter(is_active=True):
        entries.append(_entry(f"/case-studies/{case_study.slug}", "0.5", "yearly", lastmod=case_study.created_at))

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(entries)
        + "</urlset>"
    )
    return HttpResponse(xml, content_type="application/xml")
