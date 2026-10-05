from django.db import models
import uuid
from accounts.models import User, Department

class Event(models.Model):
    CATEGORY_CHOICES = [
        ("workshop", "Workshop"), ("seminar", "Seminar"), ("cultural", "Cultural"),
        ("sports", "Sports"), ("examination", "Examination"), ("placement", "Placement"),
        ("club", "Club"), ("academic", "Academic"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=255)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default="academic")
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
