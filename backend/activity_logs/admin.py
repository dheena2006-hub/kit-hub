from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("admin", "action", "module", "created_at")
    list_filter = ("module", "created_at")
    readonly_fields = ("id", "created_at")
