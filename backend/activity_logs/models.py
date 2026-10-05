from django.db import models
import uuid
from accounts.models import User

class ActivityLog(models.Model):
    MODULE_CHOICES = [
        ("users", "Users"), ("announcements", "Announcements"), ("events", "Events"),
        ("documents", "Documents"), ("placements", "Placements"), ("requests", "Requests"),
        ("staff", "Staff"), ("settings", "Settings"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="activity_logs")
    action = models.CharField(max_length=255)
    module = models.CharField(max_length=32, choices=MODULE_CHOICES)
    target_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.admin.name if self.admin else 'Unknown'} - {self.action}"
