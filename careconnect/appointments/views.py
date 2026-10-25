
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from doctors.models import Doctor
from .models import Appointment


TIME_SLOTS = [
    "5:00 PM - 5:30 PM",
    "5:30 PM - 6:00 PM",
    "6:00 PM - 6:30 PM",
    "7:00 PM - 7:30 PM",
]


def appointment_end_datetime(appointment):

    try:
        end_text = appointment.time_slot.split(" - ")[-1].strip()
        end_time = datetime.strptime(end_text, "%I:%M %p").time()
    except (ValueError, AttributeError):
        return None

    end_datetime = datetime.combine(
        appointment.appointment_date,
        end_time
    )

    return timezone.make_aware(
        end_datetime,
        timezone.get_current_timezone()
    )


def update_expired_appointments(patient):
    """Mark the patient's expired active appointments as completed."""
    now = timezone.now()

    appointments = Appointment.objects.filter(
        patient=patient,
        status__in=["Booked", "Confirmed", "Pending"]
    )

    for appointment in appointments:
        end_datetime = appointment_end_datetime(appointment)

        if end_datetime and end_datetime <= now:
            appointment.status = "Completed"
            appointment.save(update_fields=["status"])


@login_required
def book_appointment(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)

    today = timezone.localdate()
    selected_date = today
    date_text = request.GET.get("date", "").strip()

    if date_text:
        try:
            selected_date = datetime.strptime(
                date_text, "%Y-%m-%d"
            ).date()
        except ValueError:
            selected_date = today

    if selected_date < today:
        selected_date = today

    # Get all active bookings for this doctor and selected date.
    booked_slots = set(
        Appointment.objects.filter(
            doctor=doctor,
            appointment_date=selected_date,
        ).exclude(
            status="Cancelled"
        ).values_list("time_slot", flat=True)
    )

    if request.method == "POST":
        date_text = request.POST.get(
            "appointment_date", ""
        ).strip()

        slot = request.POST.get("time_slot", "").strip()

        try:
            appointment_date = datetime.strptime(
                date_text, "%Y-%m-%d"
            ).date()
        except ValueError:
            messages.error(
                request,
                "Please select a valid appointment date."
            )
            return redirect(
                "book_appointment",
                doctor_pk=doctor.pk
            )

        if appointment_date < today:
            messages.error(
                request,
                "Past dates are not allowed."
            )
            return redirect(
                "book_appointment",
                doctor_pk=doctor.pk
            )

        if slot not in TIME_SLOTS:
            messages.error(
                request,
                "Please select a valid time slot."
            )
            return redirect(
                "book_appointment",
                doctor_pk=doctor.pk
            )

        try:
            end_text = slot.split(" - ")[-1].strip()
            end_time = datetime.strptime(
                end_text, "%I:%M %p"
            ).time()
        except ValueError:
            messages.error(
                request,
                "Invalid time slot."
            )
            return redirect(
                "book_appointment",
                doctor_pk=doctor.pk
            )

        slot_end = timezone.make_aware(
            datetime.combine(appointment_date, end_time),
            timezone.get_current_timezone()
        )

        if slot_end <= timezone.now():
            messages.error(
                request,
                "This appointment time has passed."
            )
            return redirect(
                "book_appointment",
                doctor_pk=doctor.pk
            )

        try:
            with transaction.atomic():
                already_booked = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=appointment_date,
                    time_slot=slot,
                ).exclude(
                    status="Cancelled"
                ).exists()

                if already_booked:
                    messages.error(
                        request,
                        "This slot is already booked. "
                        "Please choose another time."
                    )
                    return redirect(
                        f"/appointments/book/{doctor.pk}/?date="
                        f"{appointment_date.isoformat()}"
                    )

                Appointment.objects.create(
                    patient=request.user,
                    doctor=doctor,
                    appointment_date=appointment_date,
                    time_slot=slot,
                    status="Booked",
                )

        except IntegrityError:
            messages.error(
                request,
                "Another user just booked this slot. "
                "Please choose another time."
            )
            return redirect(
                f"/appointments/book/{doctor.pk}/?date="
                f"{appointment_date.isoformat()}"
            )

        messages.success(
            request,
            "Appointment booked successfully!"
        )
        return redirect("my_appointments")

    # Refresh booked slots for the date shown on the page.
    booked_slots = set(
        Appointment.objects.filter(
            doctor=doctor,
            appointment_date=selected_date,
        ).exclude(
            status="Cancelled"
        ).values_list("time_slot", flat=True)
    )

    return render(
        request,
        "appointments/book_appointment.html",
        {
            "doctor": doctor,
            "today": today.isoformat(),
            "selected_date": selected_date.isoformat(),
            "time_slots": TIME_SLOTS,
            "booked_slots": booked_slots,
        }
    )


@login_required
def my_appointments_view(request):
    update_expired_appointments(request.user)

    appointments = Appointment.objects.filter(
        patient=request.user,
        status__in=["Booked", "Confirmed", "Pending"]
    ).select_related(
        "doctor"
    ).order_by(
        "appointment_date", "created_at"
    )

    now = timezone.now()

    upcoming = [
        app for app in appointments
        if appointment_end_datetime(app)
        and appointment_end_datetime(app) > now
    ]

    return render(
        request,
        "appointments/my_appointments.html",
        {"appointments": upcoming}
    )


@login_required
def cancel_appointment(request, appointment_id):
    if request.method != "POST":
        return redirect("my_appointments")

    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
        patient=request.user
    )

    end_datetime = appointment_end_datetime(appointment)

    if appointment.status not in [
        "Booked", "Confirmed", "Pending"
    ]:
        messages.error(
            request,
            "This appointment cannot be cancelled."
        )
    elif not end_datetime or end_datetime <= timezone.now():
        messages.error(
            request,
            "Past appointments cannot be cancelled."
        )
    else:
        appointment.status = "Cancelled"
        appointment.save(update_fields=["status"])

        messages.success(
            request,
            "Appointment cancelled successfully."
        )

    return redirect("my_appointments")
