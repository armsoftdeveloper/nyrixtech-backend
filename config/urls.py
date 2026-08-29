from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .sitemap_view import sitemap_xml

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap_xml, name="sitemap"),

    path("api/auth/", include("users.urls")),
    path("api/audits/", include("audits.urls")),
    path("api/", include("leads.urls")),               # /api/leads/, /api/contact/
    path("api/", include("services.urls")),            # /api/services/, /api/plans/, /api/faqs/ ...
    path("api/tickets/", include("tickets.urls")),
    path("api/appointments/", include("appointments.urls")),
    path("api/blog/", include("blog.urls")),
    path("api/documents/", include("documents.urls")),
    path("api/dashboard/", include("dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
