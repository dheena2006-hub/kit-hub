from rest_framework import viewsets, permissions
from .models import StudentRequest
from .serializers import StudentRequestSerializer

class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.student == request.user or getattr(request.user, "role", None) in ("admin", "dept_admin", "superadmin")
        return getattr(request.user, "role", None) in ("admin", "dept_admin", "superadmin")

class StudentRequestViewSet(viewsets.ModelViewSet):
    serializer_class = StudentRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    filterset_fields = ["category", "status"]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) in ("admin", "dept_admin", "superadmin"):
            return StudentRequest.objects.all().order_by("-created_at")
        return StudentRequest.objects.filter(student=user).order_by("-created_at")
