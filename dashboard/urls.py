from django.urls import path
from .views import AdminDashboardView, ClientDashboardView

urlpatterns = [
    path("", AdminDashboardView.as_view(), name="dashboard-admin"),
    path("client/", ClientDashboardView.as_view(), name="dashboard-client"),
]
