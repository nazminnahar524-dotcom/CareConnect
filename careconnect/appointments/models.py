
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from doctors.models import Doctor


class Appointment(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=50)

    status = models.CharField(
        max_length=30,
        choices=[
            ("Booked", "Booked"),
            ("Cancelled", "Cancelled"),
            ("Completed", "Completed"),
        ],
        default="Booked"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "doctor",
                    "appointment_date",
                    "time_slot",
                ],
                condition=~Q(status="Cancelled"),
                name="unique_active_doctor_time_slot",
            )
        ]

    def __str__(self):
        return (
            f"{self.patient.username} -> "
            f"{self.doctor.name} ({self.appointment_date})"
        )
