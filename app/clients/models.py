from django.db import models
from django.core.validators import RegexValidator


class Client(models.Model):
    """
    Model representing a client.

    Attributes:
        full_name (str): The full name of the client.
        email (str): The email address of the client.
        phone (str): The phone number of the client (optional).

    Methods:
        __str__(): Returns the full name of the client as a string.
    """

    full_name = models.CharField(
        max_length=255,
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
