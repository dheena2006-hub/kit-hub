from django.db import models
import uuid
from accounts.models import User, Department

class Placement(models.Model):
    JOB_TYPE_CHOICES = [("full-time", "Full-time"), ("internship", "Internship"), ("part-time", "Part-time")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255)
    job_role = models.CharField(max_length=255)
    job_type = models.CharField(max_length=32, choices=JOB_TYPE_CHOICES, default="internship")
    description = models.TextField()
    eligibility = models.TextField(blank=True)
    required_skills = models.TextField(blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    application_url = models.URLField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_role}"
