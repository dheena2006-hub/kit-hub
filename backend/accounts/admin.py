from django.contrib import admin
from .models import User, Department

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "role", "status", "department")

@admin.register(Department)
class DeptAdmin(admin.ModelAdmin):
    list_display = ("department_code", "department_name", "hod_name")
