from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.utils.dateparse import parse_date
from animals.models import AdoptionRequest, Donation


class AdminCustomReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        start_date = request.query_params.get('from')
        end_date = request.query_params.get('to')

        filters = {}
        if start_date and end_date:
            filters['created_at__range'] = [parse_date(start_date), parse_date(end_date)]

        # 🐾 Adoption stats
        adoptions = AdoptionRequest.objects.filter(**filters)
        adoption_success = adoptions.filter(status="Approved").count()
        adoption_pending = adoptions.filter(status="Pending").count()

        # 💰 Donation stats
        donations = Donation.objects.filter(**filters)
        total_donated = donations.aggregate(total=Sum('amount'))['total'] or 0
        donation_count = donations.count()

        # 🧾 Report Output
        report = {
            "adoption_report": {
                "approved": adoption_success,
                "pending": adoption_pending,
                "total": adoptions.count(),
            },
            "donation_report": {
                "total_amount": float(total_donated),
                "total_donations": donation_count,
            }
        }

        return Response(report)