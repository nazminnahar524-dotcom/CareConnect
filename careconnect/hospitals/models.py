from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    location = models.CharField(max_length=150, default="Dhanmondi, Dhaka")
    image = models.ImageField(upload_to='hospitals/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    reviews_count = models.IntegerField(default=120)

    total_beds = models.IntegerField(default=300)
    total_doctors = models.IntegerField(default=24)
    distance = models.CharField(max_length=50, default="1.2 km away")

    helpline = models.CharField(max_length=50, default="09612-345678")
    emergency_contact = models.CharField(max_length=50, default="01713-456789")
    email = models.EmailField(default="info@labaidgroup.com")
    website = models.URLField(default="https://www.labaidgroup.com")

    description = models.TextField(blank=True)

    # Facility flags
    has_icu = models.BooleanField(default=True)
    has_ccu = models.BooleanField(default=True)
    has_nicu = models.BooleanField(default=True)
    has_emergency = models.BooleanField(default=True)
    has_ambulance = models.BooleanField(default=True)
    has_pharmacy = models.BooleanField(default=True)

    def __str__(self):
        return self.name