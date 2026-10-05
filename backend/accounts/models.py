from django.db import models
import uuid

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_code = models.CharField(max_length=32, unique=True)
    department_name = models.CharField(max_length=128)
    hod_name = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name


class User(models.Model):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("admin", "Admin"),
        ("dept_admin", "Department Admin"),
        ("superadmin", "Super Admin"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    
    # Auth system fields (required when AUTH_USER_MODEL is set)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=200)
    roll_no = models.CharField(max_length=64, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    class_name = models.CharField(max_length=64, blank=True)
    year = models.CharField(max_length=16, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    blood_group = models.CharField(max_length=8, blank=True)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default="student")
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="pending")
    profile_photo = models.TextField(blank=True)
    linkedin = models.TextField(blank=True)
    portfolio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
