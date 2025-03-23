from django.db.models import Count
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from animals.models import AdoptionRequest


class AdoptionSuccessAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = (
            AdoptionRequest.objects
            .filter(status="Approved")
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(adoptions=Count("id"))
            .order_by("month")
        )
        return Response(data)