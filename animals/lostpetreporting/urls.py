from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LostPetReportViewSet

router = DefaultRouter()
router.register(r'lost-pets', LostPetReportViewSet, basename='lost-pet')

urlpatterns = [
    path('', include(router.urls)),
]