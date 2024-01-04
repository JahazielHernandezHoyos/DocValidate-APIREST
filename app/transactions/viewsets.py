from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Transaction
from .serializers import TransactionSerializer, TransactionCreateSerializer
from utils.viewsets import BaseViewSet


class TransactionListCreateView(mixins.ListModelMixin, BaseViewSet):
    """
    View for listing and creating transactions.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]


class TransactionDetailView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """
    View for retrieving, updating, and deleting a single transaction.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        """
        Returns the serializer class based on the request method.
        If the request method is POST, it returns TransactionCreateSerializer.
        Otherwise, it returns TransactionSerializer.
        """
        if self.request.method == "POST":
            return TransactionCreateSerializer
        return TransactionSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests and creates a new transaction.
        """
        return self.create(request, *args, **kwargs)