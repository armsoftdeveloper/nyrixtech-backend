from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, TicketMessageViewSet

router = DefaultRouter()
router.register("messages", TicketMessageViewSet, basename="ticket-message")
router.register("", TicketViewSet, basename="ticket")
urlpatterns = router.urls
