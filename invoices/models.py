from django.db import models


class Invoice(models.Model):

    original_filename = models.CharField(max_length=255)

    storage_path = models.CharField(
        max_length=500
    )

    extracted_field = models.CharField(
        max_length=255
    )

    extracted_value = models.TextField(
        blank=True,
        null=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.original_filename