
from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from doctors.models import Doctor
from .models import Appointment


def appointment_end_datetime(appointment):
    """Return the appointment's scheduled end datetime."""
    try:
        end_text = appointment.time_slot.split(" - ")[-1].strip()
        end_time = datetime.strptime(end_text, "%I:%M %p").time()
    except (ValueError, AttributeError):
        # All appointment slots should use the format:
        # 5:00 PM - 5:30 PM
        return None

    end_datetime = datetime.combine(
        appointment.appointment_date, end_time
    )
    return timezone.make_aware(
        end_datetime, timezone.get_current_timezone()
    )


def update_expired_appointments(patient):
    """Mark expired Pending/Confirmed appointments as Completed."""
    now = timezone.now()

    appointments = Appointment.objects.filter(
        patient=patient,
        status__in=["Pending", "Confirmed"]
    )

    for appointment in appointments:
        end_datetime = appointment_end_datetime(appointment)

        if end_datetime and end_datetime <= now:
            appointment.status = "Completed"
            appointment.save(update_fields=["status"])


@login_required
def book_appointment(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)

    if request.method == "POST":
        date_text = request.POST.get("appointment_date", "").strip()
        slot = request.POST.get("time_slot", "").strip()

        try:
            appointment_date = datetime.strptime(
                date_text, "%Y-%m-%d"
            ).date()
        except ValueError:
            messages.error(request, "Please select a valid appointment date.")
            return redirect("book_appointment", doctor_pk=doctor.pk)

        if appointment_date < timezone.localdate():
            messages.error(request, "Past dates are not allowed.")
            return redirect("book_appointment", doctor_pk=doctor.pk)

        if not slot:
            messages.error(request, "Please select a time slot.")
            return redirect("book_appointment", doctor_pk=doctor.pk)

        # Prevent booking a time slot that has already ended today.
        try:
            end_text = slot.split(" - ")[-1].strip()
            end_time = datetime.strptime(end_text, "%I:%M %p").time()
        except ValueError:
            messages.error(request, "Invalid time slot.")
            return redirect("book_appointment", doctor_pk=doctor.pk)

        slot_end = timezone.make_aware(
            datetime.combine(appointment_date, end_time),
            timezone.get_current_timezone()
        )

        if slot_end <= timezone.now():
            messages.error(request, "This appointment time has passed.")
            return redirect("book_appointment", doctor_pk=doctor.pk)

        # Prevent another active booking for the same doctor and slot.
        with transaction.atomic():
            already_booked = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                time_slot=slot,
            ).exclude(status="Cancelled").exists()

            if already_booked:
                messages.error(
                    request,
                    "This slot is already booked. Please choose another."
                )
                return redirect("book_appointment", doctor_pk=doctor.pk)

            Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                appointment_date=appointment_date,
                time_slot=slot,
                status="Confirmed",
            )

        messages.success(request, "Appointment booked successfully!")
        return redirect("my_appointments")

    return render(request, "appointments/book_appointment.html", {
        "doctor": doctor,
        "today": timezone.localdate().isoformat(),
    })


@login_required
def my_appointments_view(request):
    update_expired_appointments(request.user)

    appointments = Appointment.objects.filter(
        patient=request.user,
        status__in=["Pending", "Confirmed"]
    ).select_related("doctor").order_by(
        "appointment_date", "created_at"
    )

    # Only show appointments whose scheduled end is still in the future.
    upcoming = [
        app for app in appointments
        if appointment_end_datetime(app)
        and appointment_end_datetime(app) > timezone.now()
    ]

    return render(request, "appointments/my_appointments.html", {
        "appointments": upcoming
    })


@login_required
def appointment_history_view(request):
    update_expired_appointments(request.user)

    appointments = Appointment.objects.filter(
        patient=request.user
    ).select_related("doctor").order_by(
        "-appointment_date", "-created_at"
    )

    now = timezone.now()
    history = []

    for app in appointments:
        end_datetime = appointment_end_datetime(app)

        if (
            app.status in ["Cancelled", "Completed"]
            or (end_datetime and end_datetime <= now)
        ):
            history.append(app)

    return render(request, "appointments/appointment_history.html", {
        "appointments": history
    })


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

    if appointment.status not in ["Pending", "Confirmed"]:
        messages.error(request, "This appointment cannot be cancelled.")
    elif not end_datetime or end_datetime <= timezone.now():
        messages.error(request, "Past appointments cannot be cancelled.")
    else:
        appointment.status = "Cancelled"
        appointment.save(update_fields=["status"])
        messages.success(request, "Appointment cancelled successfully.")

    return redirect("my_appointments")


