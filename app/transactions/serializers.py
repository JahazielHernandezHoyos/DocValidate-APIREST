from rest_framework import serializers
from .models import Transaction
from utils.processing_images import validate_image, base64_to_image
from django.core.files.uploadedfile import TemporaryUploadedFile


class TransactionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating a transaction.

    This serializer is used to validate and serialize data when creating a transaction.
    It provides custom validation for image files and ensures that both frontside and backside images are provided.

    Attributes:
        model (django.db.models.Model): The model class to be used for serialization.
        fields (list): The fields to be included in the serialized representation.

    Methods:
        validate_image(image, max_size_mb, min_resolution, max_resolution):
            Custom validation for image files.
        validate(data):
            Custom validation to ensure that both frontside and backside images are provided.
    """

    class Meta:
        """
        The Meta class provides metadata for the TransactionCreateSerializer.
        It specifies the model and fields to be used for serialization.
        """

        model = Transaction
        fields = ["client", "image_frontside", "image_backside"]

    def validate(self, data):
        """
        Custom validation to ensure that both frontside and backside images are provided.

        Args:
            data (dict): The data to be validated.

        Raises:
            serializers.ValidationError: If either the frontside or backside image is missing.

        Returns:
            dict: The validated data.
        """
        image_frontside = data.get("image_frontside")
        image_backside = data.get("image_backside")
        if not image_frontside:
            Transaction.objects.create(
                client=data["client"],
                image_frontside=None,
                image_backside=None,
                result=False,
                error_code=4,
                details="Frontside image is missing.",
            )
            raise serializers.ValidationError("Frontside image is missing.")
        elif not image_backside:
            Transaction.objects.create(
                client=data["client"],
                image_frontside=None,
                image_backside=None,
                result=False,
                error_code=5,
                details="Backside image is missing.",
            )
            raise serializers.ValidationError("Backside image is missing.")
        # Validate the images individually
        data["image_frontside"] = validate_image(
            client=data["client"],
            image=image_frontside,
            max_size_mb=4,
            min_resolution=(224, 224),
            max_resolution=(3840, 2160),
        )
        data["image_backside"] = validate_image(
            client=data["client"],
            image=image_backside,
            max_size_mb=4,
            min_resolution=(224, 224),
            max_resolution=(3840, 2160),
        )

        if isinstance(data["image_frontside"], dict):
            Transaction.objects.create(
                client=data["client"],
                image_frontside=image_frontside,
                image_backside=image_backside,
                result=False,
                error_code=data["image_frontside"]["error_code"],
                details=data["image_frontside"]["details"],
            )
            raise serializers.ValidationError(data["image_frontside"]["details"])
        elif isinstance(data["image_backside"], dict):
            Transaction.objects.create(
                client=data["client"],
                image_frontside=image_frontside,
                image_backside=image_backside,
                result=False,
                error_code=data["image_backside"]["error_code"],
                details=data["image_backside"]["details"],
            )
            raise serializers.ValidationError(data["image_backside"]["details"])

        return data


def to_internal_value(self, data):
    """
    Convert base64 image strings to Image instances.

    Args:
        data (dict): The data to be converted.

    Returns:
        dict: The converted data.
    """
    if "image_frontside" in data and isinstance(data["image_frontside"], str):
        data["image_frontside"] = base64_to_image(data["image_frontside"])

    if "image_backside" in data and isinstance(data["image_backside"], str):
        data["image_backside"] = base64_to_image(data["image_backside"])

    return super().to_internal_value(data)


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer class for a transaction.

    This serializer is used to serialize data when retrieving, updating, and deleting a transaction.

    Attributes:
        model (django.db.models.Model): The model class to be used for serialization.
        fields (list): The fields to be included in the serialized representation.
    """

    class Meta:
        """
        The Meta class provides metadata for the TransactionSerializer.
        It specifies the model and fields to be used for serialization.
        """

        model = Transaction
        fields = "__all__"
        depth = 1