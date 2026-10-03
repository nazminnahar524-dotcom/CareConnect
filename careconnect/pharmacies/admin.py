from django.contrib import admin
from .models import Pharmacy, SavedPharmacy


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'district',
        'area',
        'phone',
        'verified',
        'is_24_7',
        'home_delivery',
        'online_order',
    )

    list_filter = (
        'verified',
        'is_24_7',
        'emergency',
        'home_delivery',
        'online_order',
        'medicine_available',
        'district',
    )

    search_fields = (
        'name',
        'address',
        'district',
        'area',
        'phone',
        'license_number',
    )

    ordering = ('name',)


@admin.register(SavedPharmacy)
class SavedPharmacyAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'pharmacy',
        'saved_at',
    )

    search_fields = (
        'user__username',
        'pharmacy__name',
    )

    ordering = ('-saved_at',)