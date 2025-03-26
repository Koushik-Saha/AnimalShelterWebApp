from django.urls import path
from .views import (
    CreateBehaviorAssessmentView,
    ListBehaviorAssessmentsView,
    BehaviorAssessmentDetailView, EnrichmentActivityCreateView, EnrichmentActivityListView, TrainingNoteListView,
    TrainingNoteCreateView, TrainingNoteDetailView,
)

urlpatterns = [
    path('create/', CreateBehaviorAssessmentView.as_view(), name='create-behavior'),
    path('animal/<int:animal_id>/', ListBehaviorAssessmentsView.as_view(), name='list-behaviors'),
    path('<int:pk>/', BehaviorAssessmentDetailView.as_view(), name='behavior-detail'),

    path("enrichment/create/", EnrichmentActivityCreateView.as_view(), name="enrichment-create"),
    path("enrichment/list/", EnrichmentActivityListView.as_view(), name="enrichment-list"),

    path('training-notes/', TrainingNoteListView.as_view(), name='training-note-list'),
    path('training-notes/create/', TrainingNoteCreateView.as_view(), name='training-note-create'),
    path('training-notes/<int:pk>/', TrainingNoteDetailView.as_view(), name='training-note-detail'),
]