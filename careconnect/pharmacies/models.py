from django.conf import settings
from django.db import models


class Pharmacy(models.Model):
    # =========================
    # BASIC INFORMATION
    # =========================

    name = models.CharField(max_length=200)

    license_number = models.CharField(
        max_length=100,
        blank=True
    )

    license_status = models.CharField(
        max_length=50,
        blank=True
    )

    # =========================
    # ADDRESS
    # =========================

    address = models.TextField()

    division = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    area = models.CharField(
        max_length=100,
        blank=True
    )

    # =========================
    # LOCATION
    # =========================

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    # =========================
    # CONTACT
    # =========================

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    # =========================
    # OPENING HOURS
    # =========================

    opening_time = models.TimeField(
        blank=True,
        null=True
    )

    closing_time = models.TimeField(
        blank=True,
        null=True
    )

    is_24_7 = models.BooleanField(
        default=False
    )

    emergency = models.BooleanField(
        default=False
    )

    # =========================
    # SERVICES
    # =========================

    home_delivery = models.BooleanField(
        default=False
    )

    online_order = models.BooleanField(
        default=False
    )

    medicine_available = models.BooleanField(
        default=True
    )

    # =========================
    # CARECONNECT VERIFICATION
    # =========================

    verified = models.BooleanField(
        default=False
    )

    # =========================
    # GOOGLE PLACE IDENTIFIER
    # =========================

    google_place_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )

    # =========================
    # TIMESTAMPS
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class SavedPharmacy(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_pharmacies'
    )

    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name='saved_by'
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'pharmacy'],
                name='unique_saved_pharmacy'
            )
        ]

        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.pharmacy.name}"