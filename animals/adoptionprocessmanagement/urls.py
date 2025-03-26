from django.urls import path
from .views import AdoptionApplicationCreateView, AdoptionApplicationListView, AdoptionApplicationDetailView, \
    AdoptionApplicationUpdateView, UpdateApplicationStatusView, MatchingToolCreateView, MatchingToolListView, \
    MatchingToolByUserView, AdoptionAgreementGenerateView

urlpatterns = [
    path("adoption-applications/create/", AdoptionApplicationCreateView.as_view(), name="create-adoption-application"),

    path("adoption-applications/", AdoptionApplicationListView.as_view(), name="list-adoption-applications"),
    path("adoption-applications/<int:pk>/", AdoptionApplicationDetailView.as_view(), name="detail-adoption-application"),

    path("adoption-applications/<int:pk>/update/", AdoptionApplicationUpdateView.as_view(),
         name="update-adoption-application"),

    path('adoption-applications/<int:pk>/status/', UpdateApplicationStatusView.as_view(), name="update-application-status"),

    path('adoption-applications/matching-tool/create/', MatchingToolCreateView.as_view(), name='matching-tool-create'),
    path('adoption-applications/matching-tool/list/', MatchingToolListView.as_view(), name='matching-tool-list'),
    path('adoption-applications/matching-tool/me/', MatchingToolByUserView.as_view(), name='matching-tool-me'),

    path("adoption-applications/agreements/<int:pk>/generate/", AdoptionAgreementGenerateView.as_view(), name="generate-agreement"),

]