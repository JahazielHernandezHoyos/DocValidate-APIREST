import base64
from io import BytesIO
from PIL import Image


def validate_image(client, image, max_size_mb, min_resolution, max_resolution):
    """
    Custom validation for image files.

    Args:
        client (django.contrib.auth.models.User): The client associated with the image.
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
        return {
            "result": False,
            "error_code": 1,
            "details": f"Image size exceeds the limit of {max_size_mb} MB.",
        }

    # Check the resolution
    width, height = image.image.size
    if (
        not min_resolution[0] <= width <= max_resolution[0]
        or not min_resolution[1] <= height <= max_resolution[1]
    ):
        return {
            "result": False,
            "error_code": 2,
            "details": f"Image resolution must be between {min_resolution} and {max_resolution}.",
        }

    # Check the file format
    if image.image.format not in ["JPEG", "JPG", "PNG", "BMP"]:
        return {
            "result": False,
            "error_code": 3,
            "details": "Image format must be JPEG, JPG, PNG, or BMP.",
        }

    return image


def base64_to_image(self, base64_string):
    """
    Convert base64 image string to Image instance.

    Args:
        base64_string (str): The base64-encoded image string.

    Returns:
        PIL.Image.Image: The Image instance.
    """
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image
