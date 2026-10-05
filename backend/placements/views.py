from rest_framework import viewsets, permissions
from .models import Placement
from .serializers import PlacementSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: return True
        return getattr(request.user, "role", None) in ("admin", "dept_admin", "superadmin")

class PlacementViewSet(viewsets.ModelViewSet):
    queryset = Placement.objects.all().order_by("-created_at")
    serializer_class = PlacementSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["department__id", "job_type", "deadline"]
