from rest_framework import mixins
from .models import Client
from .serializers import ClientSerializer, ClientCreateSerializer
from utils.viewsets import BaseViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny


class ClientListCreateView(
    mixins.ListModelMixin, BaseViewSet
):
    """
    View for listing and creating clients.
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


class ClientDetailView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """
    View for retrieving, updating, and deleting a single client.
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        """
        Returns the serializer class based on the request method.
        If the request method is POST, it returns ClientsCreateSerializer.
        Otherwise, it returns ClientsSerializer.
        """
        if self.request.method == "POST":
            return ClientCreateSerializer
        return ClientSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests and creates a new client.
        """
        return self.create(request, *args, **kwargs)
