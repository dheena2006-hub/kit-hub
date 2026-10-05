from rest_framework import viewsets, permissions
from .models import Staff
from .serializers import StaffSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: return True
        return getattr(request.user, "role", None) in ("admin", "dept_admin", "superadmin")

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all().order_by("name")
    serializer_class = StaffSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["department__id", "designation"]
