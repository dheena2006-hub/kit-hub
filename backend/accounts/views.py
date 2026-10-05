from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Department
from .serializers import UserSerializer, RegisterSerializer

@api_view(["POST"])
def register(request):
    s = RegisterSerializer(data=request.data)
    if not s.is_valid():
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
    data = s.validated_data
    dept = None
    if data.get("department_id"):
        try:
            dept = Department.objects.get(id=data["department_id"])
        except Department.DoesNotExist:
            return Response({"error": "department not found"}, status=400)
    u = User(name=data["name"], email=data["email"], password_hash=make_password(data["password"]),
             roll_no=data.get("roll_no", ""), department=dept, class_name=data.get("class_name", ""),
             year=data.get("year", ""), phone=data.get("phone", ""), blood_group=data.get("blood_group", ""),
             linkedin=data.get("linkedin", ""), portfolio=data.get("portfolio", ""))
    try:
        u.save()
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    return Response({"message": "Registered. Awaiting admin approval."}, status=201)

@api_view(["POST"])
def login(request):
    email = request.data.get("email", "").lower().strip()
    pwd = request.data.get("password", "")
    try:
        u = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=401)
    if not check_password(pwd, u.password_hash):
        return Response({"error": "Invalid credentials"}, status=401)
    if u.status != "approved":
        return Response({"error": f"Account is {u.status}. Login allowed only after admin approval."}, status=403)
    refresh = RefreshToken.for_user(u)
    return Response({"token": str(refresh.access_token), "user": UserSerializer(u).data})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)
