from django.urls import path
from .views import FosterApplicationCreateView, FosterApplicationListView, FosterApplicationDetailView, \
    FosterApplicationUpdateView, FosterApplicationDeleteView

urlpatterns = [
    path('create/', FosterApplicationCreateView.as_view(), name='foster-create'),
    path('', FosterApplicationListView.as_view(), name='foster-list'),
    path('<int:pk>/', FosterApplicationDetailView.as_view(), name='foster-detail'),
    path('<int:pk>/update/', FosterApplicationUpdateView.as_view(), name='foster-update'),
    path('<int:pk>/delete/', FosterApplicationDeleteView.as_view(), name='foster-delete'),
]