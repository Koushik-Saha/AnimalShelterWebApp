from rest_framework import generics, status
from .models import Animal
from .serializers import AnimalSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated



# Register a New Staff Member
@api_view(['POST'])
@permission_classes([AllowAny])
def register_staff(request):
    """Endpoint to register a staff user"""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    user.is_staff = True  # Mark as staff
    user.save()

    token, created = Token.objects.get_or_create(user=user)
    return Response({"message": "Staff registered successfully", "token": token.key}, status=status.HTTP_201_CREATED)


# Login and Get Token
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Endpoint for staff login and token retrieval"""
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None or not user.is_staff:
        return Response({"error": "Invalid credentials or not a staff user."}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_200_OK)

# List and Create Animals
class AnimalListCreateView(generics.ListCreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated]  # Require login

    def create(self, request, *args, **kwargs):
        # Check if the request contains a list of objects
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, and Delete a Single Animal
class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated]  # Require login