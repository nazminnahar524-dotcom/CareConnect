
from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor


class Appointment(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='appointments'
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='appointments'
    )
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=50)

    status = models.CharField(
        max_length=30,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Cancelled', 'Cancelled'),
            ('Completed', 'Completed'),
        ],
        default='Confirmed'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.patient.username} -> "
            f"Dr. {self.doctor.name} ({self.appointment_date})"
        )
