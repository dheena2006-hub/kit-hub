from django.db import models
import uuid
from accounts.models import User

class StudentRequest(models.Model):
    CATEGORY_CHOICES = [
        ("complaint", "Complaint"), ("leave", "Leave Request"), ("certificate", "Certificate Request"),
        ("technical", "Technical Issue"), ("academic", "Academic Request"), ("general", "General Request"),
    ]
    STATUS_CHOICES = [("pending", "Pending"), ("processing", "Processing"), ("resolved", "Resolved"), ("rejected", "Rejected")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, related_name="requests", on_delete=models.CASCADE)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField(upload_to="requests/", null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="pending")
    admin_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject}"
