from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import LostPetReport
from .serializers import LostPetReportSerializer
from ..utils import success_response, error_response
from rest_framework import status


class LostPetReportView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = LostPetReport.objects.all().order_by('-created_at')
    serializer_class = LostPetReportSerializer
    permission_classes = [permissions.AllowAny]
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