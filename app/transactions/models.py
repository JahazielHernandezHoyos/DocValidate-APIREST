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
    result = models.BooleanField()
    error_code = models.PositiveIntegerField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to validate the transaction and set the result, error code, and details.

        If both the frontside and backside images are present, the transaction is considered successful.
        Otherwise, the transaction is considered a failure and the appropriate error code and details are set.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        if self.image_frontside and self.image_backside:
            self.result = True
            self.error_code = None
            self.details = None
        else:
            self.result = False
            if not self.image_frontside:
                self.details = "Frontside image is missing."
            elif not self.image_backside:
                self.details = "Backside image is missing."
            self.error_code = 404

        super().save(*args, **kwargs)
