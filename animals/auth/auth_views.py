import stripe
from animals.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError

stripe.api_key = settings.STRIPE_SECRET_KEY

# User = settings.AUTH_USER_MODEL
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    API to register new users and assign them a role.
    Required: username, email, password
    Optional: role (defaults to 'user')
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'user')

    missing_fields = []
    if not username:
        missing_fields.append("username")
    if not email:
        missing_fields.append("email")
    if not password:
        missing_fields.append("password")

    if missing_fields:
        return Response({
            "error": f"The following field(s) are required: {', '.join(missing_fields)}"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

    # Check for existing user/email
    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(email=email).exists():
        return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)

    # Assign role and flags
    try:
        if role == 'staff':
            user.is_staff = True
            group = Group.objects.get(name="Shelter Staff")
        elif role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            group = Group.objects.get(name="Admin")
        else:
            group = Group.objects.get(name="User")
    except Group.DoesNotExist:
        return Response({
            "error": f"Group '{role}' does not exist. Please create the group first."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    user.save()
    user.groups.add(group)

    return Response({
        "message": "User registered successfully!",
        "username": user.username,
        "email": user.email,
        "role": role
    }, status=status.HTTP_201_CREATED)

# Login and Get Token
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Endpoint for staff login and token retrieval.
    Only staff users can log in through this endpoint.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    missing_fields = []
    if not username:
        missing_fields.append("username")
    if not password:
        missing_fields.append("password")

    if missing_fields:
        return Response({
            "error": f"The following field(s) are required: {', '.join(missing_fields)}"
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({
            "error": "Invalid username or password."
        }, status=status.HTTP_400_BAD_REQUEST)

    if not user.is_staff:
        return Response({
            "error": "Access denied. Only staff users are allowed to log in here."
        }, status=status.HTTP_403_FORBIDDEN)

    token, created = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "message": "Login successful.",
        "username": user.username,
        "role": user.role if hasattr(user, 'role') else "staff"
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    if not request.user.is_superuser:
        return Response({"error": "You do not have permission to view users."}, status=403)

    users = CustomUser.objects.all()
    data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        for user in users
    ]
    return Response(data)