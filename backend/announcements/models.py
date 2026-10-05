from django.db import models
import uuid
from accounts.models import User, Department

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("academic", "Academic"),
        ("examination", "Examination"),
        ("placement", "Placement"),
        ("event", "Event"),
        ("holiday", "Holiday"),
        ("emergency", "Emergency"),
        ("department", "Department"),
    ]
    PRIORITY_CHOICES = [("low", "Low"), ("normal", "Normal"), ("high", "High")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default="general")
    priority = models.CharField(max_length=16, choices=PRIORITY_CHOICES, default="normal")
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to="attachments/", null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
