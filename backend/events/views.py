from rest_framework import viewsets, permissions
from .models import Event
from .serializers import EventSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: 
            return True
        return getattr(request.user, "role", None) in ("admin", "dept_admin", "superadmin")

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("-event_date")
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["category", "department__id", "event_date"]
