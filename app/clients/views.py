from rest_framework import generics, mixins
from .models import Clients
from .serializers import ClientsSerializer, ClientsCreateSerializer

class ClientsListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    View for listing and creating clients.
    """
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer

    def get_serializer_class(self):
        """
        Returns the serializer class based on the request method.
        If the request method is POST, it returns ClientsCreateSerializer.
        Otherwise, it returns ClientsSerializer.
        """
        if self.request.method == 'POST':
            return ClientsCreateSerializer
        return ClientsSerializer

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and returns a list of clients.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests and creates a new client.
        """
        return self.create(request, *args, **kwargs)

class ClientsDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    View for retrieving, updating, and deleting a single client.
    """
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer

    def get(self, request, *args, **kwargs):
        """
        Retrieve a single client.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Update a single client.
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete a single client.
        """
        return self.destroy(request, *args, **kwargs)
