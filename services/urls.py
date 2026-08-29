from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ServicePlanViewSet, TestimonialViewSet, FAQViewSet, CaseStudyViewSet

router = DefaultRouter()
router.register("services", ServiceViewSet, basename="service")
router.register("plans", ServicePlanViewSet, basename="plan")
router.register("testimonials", TestimonialViewSet, basename="testimonial")
router.register("faqs", FAQViewSet, basename="faq")
router.register("case-studies", CaseStudyViewSet, basename="case-study")
urlpatterns = router.urls
