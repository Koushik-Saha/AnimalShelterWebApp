from django.urls import path
from .views import LostPetReportView, FoundAnimalView, MatchLostPetWithFoundAnimalsView, OwnerContactInfoView

urlpatterns = [
    path('lost-pets/', LostPetReportView.as_view(), name='lost-pet-list-create'),
    path('lost-pets/<int:pk>/', LostPetReportView.as_view(), name='lost-pet-detail-update-delete'),

    path('found-animals/', FoundAnimalView.as_view(), name='found-animal-crud'),

    path("lost-pets/<int:lost_pet_id>/match/", MatchLostPetWithFoundAnimalsView.as_view(),
         name="match-lost-found"),

    path('owner-contacts/', OwnerContactInfoView.as_view(), name='owner-contact-list-create'),
    path('owner-contacts/<int:pk>/', OwnerContactInfoView.as_view(), name='owner-contact-detail-update-delete'),

]