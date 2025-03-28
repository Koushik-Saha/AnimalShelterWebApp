from django.urls import path
from .views import LostPetReportView, FoundAnimalView

urlpatterns = [
    path('lost-pets/', LostPetReportView.as_view(), name='lost-pet-list-create'),
    path('lost-pets/<int:pk>/', LostPetReportView.as_view(), name='lost-pet-detail-update-delete'),

    path('found-animals/', FoundAnimalView.as_view(), name='found-animal-crud'),

]