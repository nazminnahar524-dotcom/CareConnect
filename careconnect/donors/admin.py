from django.contrib import admin
from .models import Donor, DonationHistory

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'blood_group', 'gender', 'area', 'district', 'is_available', 'latitude', 'longitude')
    list_editable = ('is_available',)
    list_filter = ('blood_group', 'gender', 'is_available', 'district')
    search_fields = ('full_name', 'phone_number', 'area', 'district')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'full_name', 'gender', 'blood_group', 'phone_number', 'is_available', 'last_donated')
        }),
        ('Additional Info', {
            'fields': ('age', 'email', 'whatsapp_number', 'occupation', 'about_me', 'languages')
        }),
        ('Location Information', {
            'fields': ('area', 'upazila', 'district', 'latitude', 'longitude')
        }),
    )


@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = ('donor', 'date', 'blood_group', 'location', 'organization')
    list_filter = ('blood_group', 'date')
    search_fields = ('donor__full_name', 'location', 'organization')
