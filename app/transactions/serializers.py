from PIL import Image
from rest_framework import serializers
from .models import Transaction

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
        fields = ['client', 'image_frontside', 'image_backside']

    def validate_image(self, image, max_size_mb, min_resolution, max_resolution):
        """
        Custom validation for image files.

        Args:
            image (PIL.Image.Image): The image to be validated.
            max_size_mb (int): The maximum size of the image in megabytes.
            min_resolution (tuple): The minimum resolution allowed for the image.
            max_resolution (tuple): The maximum resolution allowed for the image.

        Raises:
            serializers.ValidationError: If the image size exceeds the maximum size or if the resolution is outside the allowed range.

        Returns:
            PIL.Image.Image: The validated image.
        """
        # Check the size
        max_size_bytes = max_size_mb * 1024 * 1024
        if image.size > max_size_bytes:
            raise serializers.ValidationError(f"Image size exceeds the limit of {max_size_mb} MB.")

        # Check the resolution
        width, height = image.image.size
        if not min_resolution[0] <= width <= max_resolution[0] or not min_resolution[1] <= height <= max_resolution[1]:
            raise serializers.ValidationError(f"Image resolution must be between {min_resolution} and {max_resolution}.")

        # Check the file format
        if image.image.format not in ['JPEG', 'JPG', 'PNG', 'BMP']:
            raise serializers.ValidationError("Image format must be either JPEG, JPG, PNG, or BMP.")

        return image

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
        image_frontside = data.get('image_frontside')
        image_backside = data.get('image_backside')

        if not image_frontside:
            raise serializers.ValidationError("Frontside image is missing.")
        elif not image_backside:
            raise serializers.ValidationError("Backside image is missing.")

        # Validate the images individually
        data['image_frontside'] = self.validate_image(
            image=image_frontside,
            max_size_mb=4,  # Maximum allowed size in megabytes
            min_resolution=(224, 224),  # Minimum allowed resolution
            max_resolution=(3840, 2160)  # Maximum allowed resolution
        )
        data['image_backside'] = self.validate_image(
            image=image_backside,
            max_size_mb=4,
            min_resolution=(224, 224),
            max_resolution=(3840, 2160)
        )

        return data

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