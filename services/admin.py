from django.contrib import admin
from .models import Service, ServicePlan, Testimonial, FAQ, CaseStudy

admin.site.register(Service)
admin.site.register(ServicePlan)
admin.site.register(Testimonial)
admin.site.register(FAQ)
admin.site.register(CaseStudy)
