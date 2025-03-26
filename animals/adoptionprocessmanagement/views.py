from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from .serializers import AdoptionApplicationSerializer, AdoptionApplicationStatusSerializer, MatchingToolSerializer, \
    AdoptionAgreementSerializer, PostAdoptionFollowUpSerializer
from .models import AdoptionApplication, MatchingTool, AdoptionAgreement, PostAdoptionFollowUp
from ..models import Animal
from ..permissions import IsAdminOrShelterStaff, IsAdmin
from rest_framework.response import Response
from rest_framework import status




class AdoptionApplicationCreateView(generics.CreateAPIView):
    queryset = AdoptionApplication.objects.all().order_by('-id')
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdoptionApplicationListView(generics.ListAPIView):
    queryset = AdoptionApplication.objects.all().order_by('-id')
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrShelterStaff]


class AdoptionApplicationDetailView(generics.RetrieveAPIView):
    queryset = AdoptionApplication.objects.all()
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrShelterStaff]


class AdoptionApplicationUpdateView(generics.UpdateAPIView):
    queryset = AdoptionApplication.objects.all()
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrShelterStaff]

    def update(self, request, *args, **kwargs):
        application = self.get_object()

        if application.status != "Pending":
            return Response(
                {"error": "This application has already been processed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_status = request.data.get("status")
        if new_status not in ["Approved", "Rejected"]:
            return Response(
                {"error": "Invalid status. Must be 'Approved' or 'Rejected'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = new_status
        application.reviewed_by = request.user
        application.save()

        return Response(
            {
                "message": f"Application status updated to {new_status}",
                "application_id": application.id,
                "status": new_status,
            },
            status=status.HTTP_200_OK,
        )

class UpdateApplicationStatusView(generics.UpdateAPIView):
    queryset = AdoptionApplication.objects.all()
    serializer_class = AdoptionApplicationStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrShelterStaff]


class MatchingToolCreateView(generics.CreateAPIView):
    serializer_class = MatchingToolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(adopter=self.request.user)

class MatchingToolListView(generics.ListAPIView):
    serializer_class = MatchingToolSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MatchingTool.objects.all()

class MatchingToolByUserView(generics.RetrieveAPIView):
    serializer_class = MatchingToolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return MatchingTool.objects.get(adopter=self.request.user)

class AdoptionAgreementGenerateView(generics.UpdateAPIView):
    queryset = AdoptionApplication.objects.all()
    serializer_class = AdoptionAgreementSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def update(self, request, *args, **kwargs):
        application = self.get_object()
        agreement_text = request.data.get("agreement_text")
        animal_id = request.data.get("animal_id")  # From Postman body
        animal = get_object_or_404(Animal, id=animal_id)

        if application.status != "approved":
            return Response({"error": "Agreement can only be generated for approved applications."}, status=400)

        agreement = AdoptionAgreement.objects.create(
            user=application.user,
            animal=animal,
            agreement_text=agreement_text,
        )
        agreement.generate_pdf()

        # agreement = AdoptionAgreement.objects.create(
        #     user=application.user,
        #     animal=animal,
        #     agreement_text=agreement_text,
        # )
        # agreement.pdf_file = agreement.generate_pdf()
        # agreement.save()

        return Response({
            "message": "Adoption agreement generated successfully",
            "pdf_url": agreement.pdf_file.url if agreement.pdf_file else None
        }, status=201)


class PostAdoptionFollowUpListCreateView(generics.ListCreateAPIView):
    queryset = PostAdoptionFollowUp.objects.all()
    serializer_class = PostAdoptionFollowUpSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrShelterStaff]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostAdoptionFollowUpDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostAdoptionFollowUp.objects.all()
    serializer_class = PostAdoptionFollowUpSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrShelterStaff]