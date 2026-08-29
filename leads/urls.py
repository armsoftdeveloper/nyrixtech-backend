from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, ContactRequestViewSet

router = DefaultRouter()
router.register("leads", LeadViewSet, basename="lead")
router.register("contact", ContactRequestViewSet, basename="contact")
urlpatterns = router.urls
