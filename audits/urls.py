from rest_framework.routers import DefaultRouter
from .views import ITAuditRequestViewSet

router = DefaultRouter()
router.register("", ITAuditRequestViewSet, basename="audit")
urlpatterns = router.urls
