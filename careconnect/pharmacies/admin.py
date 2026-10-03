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

    class Media:

        css = {
            'all': (
                'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
                'pharmacies/admin_location.css',
            )
        }

        js = (
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
            'pharmacies/admin_location.js',
        )


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