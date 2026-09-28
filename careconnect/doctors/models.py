from django.db import models

# Create your models here.


class Doctor(models.Model):
    name = models.CharField(max_length=150)
    qualification = models.CharField(max_length=200)
    specialty = models.CharField(max_length=150)
    hospital_name = models.CharField(max_length=200)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    available_days = models.CharField(max_length=100) # e.g., Sat, Mon, Wed
    visiting_hours = models.CharField(max_length=100) # e.g., 5 PM - 8 PM
    phone = models.CharField(max_length=30, blank=True, null=True)

