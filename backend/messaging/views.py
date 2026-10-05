from rest_framework import viewsets, permissions
from django.db import models
from .models import Message
from .serializers import MessageSerializer

class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("created_at")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        return Message.objects.filter(models.Q(sender=u) | models.Q(receiver=u)).order_by("created_at")
