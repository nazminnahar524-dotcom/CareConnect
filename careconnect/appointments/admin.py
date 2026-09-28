from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'time_slot', 'status')
    list_filter = ('status', 'appointment_date')


from django.contrib import admin

# Register your models here.
