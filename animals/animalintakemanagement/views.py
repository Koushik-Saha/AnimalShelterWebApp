from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import AnimalIntake
from .serializers import AnimalIntakeSerializer
from .permissions import IsStaffOrAdmin  # custom permission if needed
from animals.permissions import IsStaff, IsAdmin


# ✅ Create & List
class AnimalIntakeListCreateView(generics.ListCreateAPIView):
    queryset = AnimalIntake.objects.all()
    serializer_class = AnimalIntakeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Animal intake created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ✅ Retrieve by ID
class AnimalIntakeDetailView(generics.RetrieveAPIView):
    queryset = AnimalIntake.objects.all()
    serializer_class = AnimalIntakeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


# ✅ Update by ID
class AnimalIntakeUpdateView(generics.UpdateAPIView):
    queryset = AnimalIntake.objects.all()
    serializer_class = AnimalIntakeSerializer
    permission_classes = [IsStaffOrAdmin]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Animal intake updated successfully", "data": serializer.data})
        return Response({"error": serializer.errors}, status=400)


# ✅ Delete by ID
class AnimalIntakeDeleteView(generics.DestroyAPIView):
    queryset = AnimalIntake.objects.all()
    serializer_class = AnimalIntakeSerializer
    permission_classes = [IsStaffOrAdmin]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Animal intake record deleted successfully"}, status=204)


class AnimalIntakeListView(generics.ListAPIView):
    serializer_class = AnimalIntakeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        source = self.request.query_params.get('source')
        queryset = AnimalIntake.objects.all()
        if source:
            queryset = queryset.filter(source=source)
        return queryset

class AddStayHistoryView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, pk):
        intake = get_object_or_404(AnimalIntake, pk=pk)
        history_entry = {
            "date": request.data.get("date"),
            "reason": request.data.get("reason")
        }

        if not history_entry["date"] or not history_entry["reason"]:
            return Response({"error": "Both date and reason are required."}, status=400)

        intake.stay_history.append(history_entry)
        intake.save()

        return Response({"message": "Stay history updated successfully", "history": intake.stay_history}, status=200)