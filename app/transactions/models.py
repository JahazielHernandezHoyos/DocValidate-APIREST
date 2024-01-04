from django.db import models
from clients.models import Client

class Transaction(models.Model):
    """
    Model representing a transaction.

    Attributes:
        client (ForeignKey): The client associated with the transaction.
        creation_date (DateTimeField): The date and time when the transaction was created.
        image_frontside (ImageField): The image of the front side of the transaction.
        image_backside (ImageField): The image of the back side of the transaction.
        result (BooleanField): The result of the transaction (True for success, False for failure).
        error_code (PositiveIntegerField): The error code associated with the transaction (optional).
        details (TextField): Additional details about the transaction (optional).
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    image_frontside = models.ImageField(upload_to='transaction_images/')
    image_backside = models.ImageField(upload_to='transaction_images/')
    result = models.BooleanField(default=True)
    error_code = models.PositiveIntegerField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        """
        Returns the string representation of the transaction.

        Returns:
            str: The string representation of the transaction.
        """
        return f"{self.client} - {self.creation_date}"