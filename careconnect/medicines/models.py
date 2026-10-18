
from django.db import models


class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ("brand_allopathic", "Brand Name (Allopathic)"),
        ("brand_herbal", "Brand Name (Herbal)"),
        ("generic_allopathic", "Generics (Allopathic)"),
        ("generic_herbal", "Generics (Herbal)"),
        ("drug", "Drugs"),
        ("pharmaceutical_company", "Pharmaceutical Company"),
    ]

    name = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=200, blank=True)
    generic_name = models.CharField(max_length=200, blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="brand_allopathic",
    )
    sub_category = models.CharField(max_length=100, blank=True)

    dosage_form = models.CharField(max_length=100, blank=True)
    pack_size = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)
    indication = models.TextField(blank=True)

    prescription_required = models.BooleanField(default=False)
    registration_number = models.CharField(max_length=100, blank=True)

    image = models.ImageField(
        upload_to="medicines/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PharmacyMedicine(models.Model):
    pharmacy = models.ForeignKey(
        "pharmacies.Pharmacy",
        on_delete=models.CASCADE,
        related_name="medicine_inventory",
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="pharmacy_listings",
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["medicine__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["pharmacy", "medicine"],
                name="unique_pharmacy_medicine",
            )
        ]

    def __str__(self):
        return f"{self.medicine.name} - {self.pharmacy.name}"
