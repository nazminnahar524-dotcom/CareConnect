from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'hospital_name', 'consultation_fee')
    search_fields = ('name', 'specialty', 'hospital_name')