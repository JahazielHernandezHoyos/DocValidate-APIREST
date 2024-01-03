from collections import OrderedDict
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class that adds additional metadata to the paginated response.
    """

    page_size = 35

    def get_paginated_response(self, data):
        """
        Get the paginated response with additional metadata.

        Args:
            data (list): The paginated data.

        Returns:
            Response: The paginated response with additional metadata.
        """
        return Response(
            OrderedDict(
                [
                    ("current_page", self.page.number),
                    ("pages", self.page.paginator.num_pages),
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


class BaseViewSet(viewsets.GenericViewSet):
    """
    Base viewset class that provides common functionality for other viewsets.
    """

    permission_classes = [
        AllowAny,
    ]
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    custom_serializer_class = None

    def get_serializer_class(self):
        """
        Get the serializer class based on the action.

        Returns:
            type: The serializer class.
        """
        if self.action == "list":
            if hasattr(self, "list_serializer_class"):
                return self.list_serializer_class
        if self.action == "retrieve":
            if hasattr(self, "detail_serializer_class"):
                return self.detail_serializer_class
        return super().get_serializer_class()


class PublicReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset class for public read-only operations.
    """

    permission_classes = [
        AllowAny,
    ]
    filter_backends = (filters.SearchFilter,)

    def get_serializer_class(self):
        """
        Get the serializer class based on the action.

        Returns:
            type: The serializer class.
        """
        if self.action == "retrieve":
            if hasattr(self, "detail_serializer_class"):
                return self.detail_serializer_class
        return super().get_serializer_class()


class PrivateModelViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset class for private model operations.
    """

    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = (filters.SearchFilter,)

    def get_serializer_class(self):
        """
        Get the serializer class based on the action.

        Returns:
            type: The serializer class.
        """
        if self.action == "retrieve":
            if hasattr(self, "detail_serializer_class"):
                return self.detail_serializer_class
        return super().get_serializer_class()


class OwnerBaseViewSet(viewsets.GenericViewSet):
    """
    Base viewset class for owner-based operations.
    """

    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)

    def get_serializer_class(self):
        """
        Get the serializer class based on the action.

        Returns:
            type: The serializer class.
        """
        if self.action == "list":
            if hasattr(self, "list_serializer_class"):
                return self.list_serializer_class
        if self.action == "retrieve":
            if hasattr(self, "detail_serializer_class"):
                return self.detail_serializer_class
        return super().get_serializer_class()


class OwnerModelViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    OwnerBaseViewSet,
):
    """
    Viewset class for owner-based model operations.
    """


class CrudModelViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseViewSet,
):
    """
    Viewset class for CRUD model operations.
    """
