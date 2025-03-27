from django.urls import path
from .views import FosterApplicationCreateView, FosterApplicationListView, FosterApplicationDetailView, \
    FosterApplicationUpdateView, FosterApplicationDeleteView, FosterMatchView, FosterPlacementListCreateView, \
    FosterPlacementDetailView, FosterCommunicationCreateView, FosterCommunicationListView

urlpatterns = [
    path('create/', FosterApplicationCreateView.as_view(), name='foster-create'),
    path('list', FosterApplicationListView.as_view(), name='foster-list'),
    path('details/<int:pk>/', FosterApplicationDetailView.as_view(), name='foster-detail'),
    path('<int:pk>/update/', FosterApplicationUpdateView.as_view(), name='foster-update'),
    path('<int:pk>/delete/', FosterApplicationDeleteView.as_view(), name='foster-delete'),

    path('match-foster-animals/', FosterMatchView.as_view(), name='match-foster-animals'),

    path('foster-placements/', FosterPlacementListCreateView.as_view(), name='foster-placement-list-create'),
    path('foster-placements/<int:pk>/', FosterPlacementDetailView.as_view(), name='foster-placement-detail'),

    path("communications/create/", FosterCommunicationCreateView.as_view(), name="create-foster-communication"),
    path("communications/", FosterCommunicationListView.as_view(), name="list-foster-communications"),
]