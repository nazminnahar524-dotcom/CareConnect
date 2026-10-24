
from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=150)
    qualification = models.CharField(max_length=200)
    specialty = models.CharField(max_length=150)
    consultation_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    available_days = models.CharField(max_length=100)
    visiting_hours = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    hospital = models.ForeignKey(
        'hospitals.Hospital',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctors'
    )

    photo = models.ImageField(
        upload_to='doctors/',
        blank=True,
        null=True
    )

    @property
    def hospital_name(self):
        """Return the related hospital's name for existing templates."""
        if self.hospital_id and self.hospital:
            return self.hospital.name
        return "Hospital not specified"

    def __str__(self):
        return f"{self.name} - {self.specialty}"
