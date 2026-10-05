from django.db import models
import uuid
from accounts.models import User

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ("announcement", "Announcement"), ("event", "Event"), ("message", "Message"),
        ("approval", "Approval"), ("request_update", "Request Update"), ("placement", "Placement"),
        ("emergency", "Emergency"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=32, choices=NOTIFICATION_TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.name} - {self.title}"
