
from django.contrib import admin
from .models import Medicine, PharmacyMedicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand_name",
        "generic_name",
        "manufacturer",
        "category",
        "prescription_required",
        "is_active",
    )

    search_fields = (
        "name",
        "brand_name",
        "generic_name",
        "manufacturer",
    )

    list_filter = (
        "category",
        "prescription_required",
        "is_active",
    )


@admin.register(PharmacyMedicine)
class PharmacyMedicineAdmin(admin.ModelAdmin):
    list_display = (
        "medicine",
        "pharmacy",
        "price",
        "stock_quantity",
        "is_available",
    )

    search_fields = (
        "medicine__name",
        "pharmacy__name",
    )

    list_filter = ("is_available",)
