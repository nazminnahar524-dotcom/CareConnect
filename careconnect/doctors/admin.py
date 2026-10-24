from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'hospital', 'consultation_fee')
    search_fields = ('name', 'specialty', 'hospital__name')
    fields = (
        'name',
        'qualification',
        'specialty',
        'hospital',
        'consultation_fee',
        'available_days',
        'visiting_hours',
        'phone',
        'photo',
    )
