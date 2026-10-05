import jwt, datetime
from bson import ObjectId
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from .db import users

def make_token(u):
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=settings.JWT_HOURS)
    return jwt.encode({"sub": str(u["_id"]), "role": u["role"], "exp": exp}, settings.SECRET_KEY, "HS256")

class AuthUser(dict):
    is_authenticated = True

class JWTAuth(BaseAuthentication):
    def authenticate(self, request):
        h = request.headers.get("Authorization", "")
        if not h.startswith("Bearer "): return None
        try: p = jwt.decode(h[7:], settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.PyJWTError: raise AuthenticationFailed("Invalid or expired token")
        u = users.find_one({"_id": ObjectId(p["sub"])})
        if not u or u["status"] != "approved": raise AuthenticationFailed("Account not approved")
        return AuthUser(u), None

class IsApproved(BasePermission):
    def has_permission(self, request, view): return bool(request.user)

class IsAdmin(BasePermission):
    def has_permission(self, request, view): return bool(request.user) and request.user["role"] == "admin"
