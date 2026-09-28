from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from doctors.models import Doctor

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=50) # e.g., "6:00 PM - 6:30 PM"
    status = models.CharField(
        max_length=30,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        default='Confirmed'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} -> Dr. {self.doctor.name} ({self.appointment_date})"