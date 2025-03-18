from django.urls import path
from .views import AnimalListCreateView, AnimalDetailView
from .views import register_staff, login_user


urlpatterns = [
    path('register/', register_staff, name='register_staff'),
    path('login/', login_user, name='login_user'),
    path('animals/', AnimalListCreateView.as_view(), name='animal-list'),
    path('animals/<int:pk>/', AnimalDetailView.as_view(), name='animal-detail'),
]