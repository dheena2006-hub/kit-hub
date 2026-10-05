from django.db import models
import uuid
from accounts.models import User, Department

class Document(models.Model):
    CATEGORY_CHOICES = [
        ("circular", "Circulars"), ("academic", "Academic Documents"), ("examination", "Examination Documents"),
        ("forms", "Forms"), ("regulations", "Regulations"), ("department", "Department Documents"),
        ("placement", "Placement Documents"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default="circular")
    file = models.FileField(upload_to="documents/")
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
