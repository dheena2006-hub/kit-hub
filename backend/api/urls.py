from django.urls import path
from . import views as v
urlpatterns = [
    path("register/", v.register), path("login/", v.login), path("me/", v.me),
    path("me/export/", v.export),
    path("admin/users/", v.admin_users), path("admin/users/<str:uid>/", v.admin_user),
    path("announcements/", v.announcements_view),
    path("messages/", v.messages_view), path("contacts/", v.contacts),
    path("blood/", v.blood), path("staff/", v.staff_view),
]
