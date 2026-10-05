from rest_framework.routers import DefaultRouter
from .views import StudentRequestViewSet

router = DefaultRouter()
router.register(r"requests", StudentRequestViewSet, basename="request")
urlpatterns = router.urls
