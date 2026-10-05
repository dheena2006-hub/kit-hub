from django.contrib import admin
from .models import StudentRequest

@admin.register(StudentRequest)
class StudentRequestAdmin(admin.ModelAdmin):
    list_display = ("student", "category", "subject", "status", "created_at")
    list_filter = ("category", "status", "created_at")
