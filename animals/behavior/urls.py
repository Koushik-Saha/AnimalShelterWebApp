from django.urls import path
from .views import (
    CreateBehaviorAssessmentView,
    ListBehaviorAssessmentsView,
    BehaviorAssessmentDetailView,
)

urlpatterns = [
    path('create/', CreateBehaviorAssessmentView.as_view(), name='create-behavior'),
    path('animal/<int:animal_id>/', ListBehaviorAssessmentsView.as_view(), name='list-behaviors'),
    path('<int:pk>/', BehaviorAssessmentDetailView.as_view(), name='behavior-detail'),
]