# views.py

from animals.models import AdoptionRequest, Profile
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

class ApproveAdoptionRequestView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            adoption_request = AdoptionRequest.objects.get(pk=pk)
        except AdoptionRequest.DoesNotExist:
            return Response({"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

        adoption_request.status = "Approved"
        adoption_request.save()

        # ✅ Update the user’s profile for tracking successful adoptions
        profile, created = Profile.objects.get_or_create(user=adoption_request.user)
        profile.adoption_success_count += 1
        profile.save()

        return Response({"message": "Adoption approved."}, status=status.HTTP_200_OK)