from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .ml.matcher import suggest_animals
from .models import Animal
from .serializers import AnimalSerializer

class AnimalMatchSuggestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        preferences = {
            "species": request.data.get("species"),
            "age": int(request.data.get("age", 0)),
            "temperament": request.data.get("temperament")
        }

        matched_ids = suggest_animals(preferences)
        animals = Animal.objects.filter(id__in=matched_ids)
        serializer = AnimalSerializer(animals, many=True)

        return Response({"matches": serializer.data})