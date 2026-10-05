from rest_framework import viewsets, permissions
from .models import Document
from .serializers import DocumentSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: return True
        return getattr(request.user, "role", None) in ("admin", "dept_admin", "superadmin")

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by("-created_at")
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["category", "department__id"]
