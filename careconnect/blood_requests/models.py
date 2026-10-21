
from django.conf import settings
from django.db import models


class BloodRequest(models.Model):
    BLOOD_GROUPS = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("fulfilled", "Fulfilled"),
        ("closed", "Closed"),
    ]

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blood_requests",
    )
    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUPS,
    )
    bags_needed = models.PositiveIntegerField(default=1)
    patient_relation = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=200)
    location_address = models.CharField(max_length=300)
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_number = models.CharField(max_length=20)
    needed_by = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["needed_by", "-created_at"]

    def __str__(self):
        return f"{self.blood_group} request - {self.hospital_name}"


# Create your models here.
