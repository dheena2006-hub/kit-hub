from django.urls import path, include

urlpatterns = [
	# Legacy MongoDB-based API removed from main routes to avoid import issues.
	# New Django app endpoints are registered below.
	path("api/accounts/", include("accounts.urls")),
	path("api/announcements/", include("announcements.urls")),
	path("api/events/", include("events.urls")),
	path("api/messaging/", include("messaging.urls")),
	path("api/documents/", include("documents.urls")),
	path("api/placements/", include("placements.urls")),
    path("api/staff/", include("staff.urls")),
    path("api/requests/", include("requests.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/admin/", include("activity_logs.urls")),
]
