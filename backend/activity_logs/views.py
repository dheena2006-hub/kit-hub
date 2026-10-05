from rest_framework import viewsets, permissions
from .models import ActivityLog
from .serializers import ActivityLogSerializer

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, "role", None) in ("admin", "superadmin")

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all().order_by("-created_at")
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdmin]
