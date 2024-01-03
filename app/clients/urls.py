from django.urls import path
from .views import ClientsListCreateView, ClientsDetailView

urlpatterns = [
    path('/', ClientsListCreateView.as_view(), name='Clients-list-create'),
    path('/<int:pk>/', ClientsDetailView.as_view(), name='Clients-detail'),
]
