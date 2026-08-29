from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff_role:
            return Document.objects.all()
        return Document.objects.filter(company__client_profiles__user=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff_role:
            serializer.save(uploaded_by=user)
        else:
            # Never trust a client-submitted company id — force it from the requester's
            # own profile so a client can't attach a document to another company (IDOR).
            profile = getattr(user, "client_profile", None)
            if not profile:
                raise PermissionDenied("Your account isn't linked to a company yet.")
            serializer.save(uploaded_by=user, company=profile.company)
