from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .models import LostPetReport, FoundAnimalReport, OwnerContactInfo
from .serializers import LostPetReportSerializer, FoundAnimalSerializer, OwnerContactInfoSerializer
from ..utils import success_response, error_response, match_lost_and_found
from rest_framework import status


class LostPetReportView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = LostPetReport.objects.all().order_by('-created_at')
    serializer_class = LostPetReportSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'species', 'last_seen_location']
    search_fields = ['description', 'location', 'reporter_name']
    ordering_fields = ['created_at']
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data, message="Lost pet reports fetched successfully", code=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data, message="Lost pet report retrieved",
                                code=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="Lost pet report created successfully",code=status.HTTP_201_CREATED)
        return error_response(serializer.errors, message="Validation failed",code=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="Lost pet report updated successfully",code=status.HTTP_200_OK)
        return error_response(serializer.errors, message="Update failed",code=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response("", message="Lost pet report deleted successfully",code=status.HTTP_204_NO_CONTENT)



class LostPetFilterView(ListAPIView):
    queryset = LostPetReport.objects.all().order_by("-created_at")
    serializer_class = LostPetReportSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "species", "breed", "last_seen_location"]
    ordering_fields = ["created_at", "last_seen_date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        species = self.request.query_params.get("species")
        status = self.request.query_params.get("status")
        reporter = self.request.query_params.get("reporter")

        if species:
            queryset = queryset.filter(species__iexact=species)
        if status:
            queryset = queryset.filter(status=status)
        if reporter and self.request.user.is_staff:
            queryset = queryset.filter(reporter__id=reporter)
        elif not self.request.user.is_staff:
            queryset = queryset.filter(reporter=self.request.user)

        return queryset

class FoundAnimalView(
    generics.ListCreateAPIView,
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = FoundAnimalReport.objects.all().order_by('-created_at')
    serializer_class = FoundAnimalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'species', 'found_location']
    search_fields = ['description', 'found_location', 'species', 'breed']

    def get_queryset(self):
        return FoundAnimalReport.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(finder=self.request.user)

class MatchLostPetWithFoundAnimalsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, lost_pet_id):
        try:
            lost_pet = LostPetReport.objects.get(id=lost_pet_id)
        except LostPetReport.DoesNotExist:
            return error_response("Lost pet not found.", status.HTTP_404_NOT_FOUND)

        found_animals = FoundAnimalReport.objects.filter(status="unclaimed")
        matches = match_lost_and_found(lost_pet, found_animals)
        serializer = FoundAnimalSerializer(matches, many=True)

        return success_response("Matching found animals", serializer.data)

class OwnerContactInfoView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = OwnerContactInfo.objects.all().order_by('-created_at')
    serializer_class = OwnerContactInfoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['email', 'phone_number']
    search_fields = ['email', 'phone_number', 'address']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return success_response("Owner contact information created successfully", serializer.data)
        return error_response("Validation failed", serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return success_response("Owner contact information updated successfully", serializer.data)
        return error_response("Validation failed", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response("Owner contact information deleted successfully")