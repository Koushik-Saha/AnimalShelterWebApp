import csv

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from animals.models import AdoptionRequest, Donation


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

class DonationTrendAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        donations = (
            Donation.objects
            .filter(status="Completed")
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total_donated=Sum("amount"))
            .order_by("month")
        )
        return Response(donations)

class DonationCSVExportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        donations = Donation.objects.filter(status="Completed").order_by("created_at")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="donation_report.csv"'

        writer = csv.writer(response)
        writer.writerow(["User", "Amount", "Transaction ID", "Status", "Date"])
        for d in donations:
            writer.writerow([d.user.username if d.user else "Anonymous", d.amount, d.transaction_id, d.status, d.created_at])

        return response