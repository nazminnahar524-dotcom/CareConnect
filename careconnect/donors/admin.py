from django.contrib import admin
from .models import Donor, DonationHistory


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'blood_group', 'gender', 'area', 'is_available', 'phone_number')
    list_filter = ('blood_group', 'gender', 'is_available', 'district')
    search_fields = ('full_name', 'phone_number', 'area')


@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = ('donor', 'date', 'blood_group', 'location', 'organization')
    list_filter = ('blood_group', 'date')
    search_fields = ('donor__full_name', 'location', 'organization')
