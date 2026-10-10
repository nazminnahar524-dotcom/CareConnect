from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile', null=True, blank=True)
    full_name = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='donor_photos/', null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField(default=24)
    district = models.CharField(max_length=50, default='Dhaka')
    upazila = models.CharField(max_length=50, default='Dhanmondi')
    area = models.CharField(max_length=100, default='Dhanmondi, Dhaka')
    is_available = models.BooleanField(default=True)
    last_donated_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, default='+880 1712-345678')
    whatsapp_number = models.CharField(max_length=20, default='+880 1712-345678')
    email = models.EmailField(default='donor@gmail.com')
    date_joined = models.DateField(auto_now_add=True)
    occupation = models.CharField(max_length=100, default='Software Engineer')
    languages = models.CharField(max_length=100, default='Bangla, English')
    about_me = models.TextField(default='I am happy to help save lives. Feel free to contact me.')
    total_donations = models.IntegerField(default=5)
    distance_km = models.FloatField(default=0.8)

    def __str__(self):
        return f"{self.full_name} ({self.blood_group})"

class DonationHistory(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donation_histories')
    date = models.DateField()
    blood_group = models.CharField(max_length=5)
    location = models.CharField(max_length=150)
    organization = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.donor.full_name} - {self.date}"