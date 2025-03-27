from django.urls import path
from .views import FosterApplicationCreateView

urlpatterns = [
    path('create/', FosterApplicationCreateView.as_view(), name='foster-application-create'),
]