from django.db import models
from django.contrib.auth.models import User


class Donor(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    profile_photo = models.ImageField(
        upload_to='donor_photos/',
        blank=True,
        null=True,
    )
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    languages = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=100)
    upazila = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    last_donated = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.blood_group})"


class DonationHistory(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donation_history')
    date = models.DateField()
    blood_group = models.CharField(max_length=5, choices=Donor.BLOOD_GROUP_CHOICES)
    location = models.CharField(max_length=200)
    organization = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.donor.full_name} - {self.date}"