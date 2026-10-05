from rest_framework import viewsets, permissions
from .models import Announcement
from .serializers import AnnouncementSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: 
            return True
        # Check if user is authenticated and has admin role
        if hasattr(request.user, 'role'):
            return request.user.role in ("admin", "dept_admin", "superadmin")
        return False

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by("-created_at")
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["category", "department__id", "is_pinned"]
