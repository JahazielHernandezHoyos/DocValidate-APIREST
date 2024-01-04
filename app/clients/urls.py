from django.urls import path, include
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r"clients", viewsets.ClientListCreateView, basename="clients")
router.register(r"client", viewsets.ClientDetailView, basename="client")

urlpatterns = [path("", include(router.urls))]
