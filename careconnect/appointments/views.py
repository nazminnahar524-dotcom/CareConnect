
from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from doctors.models import Doctor
from .models import Appointment


def get_appointment_end(app):
    """
    Calculate the appointment's ending date and time.
    Example: 6:00 PM - 6:30 PM -> 6:30 PM
    """
    try:
        end_time_text = app.time_slot.split(" - ")[-1].strip()
        end_time = datetime.strptime(end_time_text, "%I:%M %p").time()
    except ValueError:
        # Fallback if the stored time slot has an unexpected format.
        end_time = time.max

    end_datetime = datetime.combine(
        app.appointment_date,
        end_time
    )

    return timezone.make_aware(
        end_datetime,
        timezone.get_current_timezone()
    )


@login_required
def book_appointment(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)

    if request.method == 'POST':
        date_text = request.POST.get('appointment_date', '').strip()
        slot = request.POST.get('time_slot', '').strip()

        try:
            appointment_date = datetime.strptime(
                date_text, '%Y-%m-%d'
            ).date()
        except ValueError:
            messages.error(
                request,
                'Please select a valid appointment date.'
            )
            return render(
                request,
                'appointments/book_appointment.html',
                {'doctor': doctor, 'today': timezone.localdate().isoformat()}
            )

        if appointment_date < timezone.localdate():
            messages.error(
                request,
                'You cannot book an appointment for a past date.'
            )
            return render(
                request,
                'appointments/book_appointment.html',
                {'doctor': doctor, 'today': timezone.localdate().isoformat()}
            )

        if not slot:
            messages.error(request, 'Please select a time slot.')
            return render(
                request,
                'appointments/book_appointment.html',
                {'doctor': doctor, 'today': timezone.localdate().isoformat()}
            )

        # Prevent booking a time slot that has already passed today.
        try:
            end_time_text = slot.split(" - ")[-1].strip()
            end_time = datetime.strptime(
                end_time_text, "%I:%M %p"
            ).time()

            appointment_end = timezone.make_aware(
                datetime.combine(appointment_date, end_time),
                timezone.get_current_timezone()
            )

            if appointment_end <= timezone.now():
                messages.error(
                    request,
                    'This appointment time has already passed.'
                )
                return render(
                    request,
                    'appointments/book_appointment.html',
                    {
                        'doctor': doctor,
                        'today': timezone.localdate().isoformat()
                    }
                )
        except ValueError:
            messages.error(request, 'Please select a valid time slot.')
            return render(
                request,
                'appointments/book_appointment.html',
                {'doctor': doctor, 'today': timezone.localdate().isoformat()}
            )

        already_booked = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            time_slot=slot,
        ).exclude(status='Cancelled').exists()

        if already_booked:
            messages.error(
                request,
                'This time slot is already booked. Please choose another slot.'
            )
            return render(
                request,
                'appointments/book_appointment.html',
                {'doctor': doctor, 'today': timezone.localdate().isoformat()}
            )

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            appointment_date=appointment_date,
            time_slot=slot,
            status='Confirmed',
        )

        messages.success(
            request,
            f'Appointment booked successfully with Dr. {doctor.name}.'
        )
        return redirect('my_appointments')

    return render(request, 'appointments/book_appointment.html', {
        'doctor': doctor,
        'today': timezone.localdate().isoformat(),
    })


@login_required
def my_appointments_view(request):
    all_appointments = (
        Appointment.objects
        .filter(patient=request.user)
        .select_related('doctor')
        .order_by('appointment_date', 'created_at')
    )

    now = timezone.now()
    upcoming_appointments = []

    for app in all_appointments:
        if get_appointment_end(app) > now:
            upcoming_appointments.append(app)

    return render(request, 'appointments/my_appointments.html', {
        'appointments': upcoming_appointments,
    })


@login_required
def appointment_history_view(request):
    all_appointments = (
        Appointment.objects
        .filter(patient=request.user)
        .select_related('doctor')
        .order_by('-appointment_date', '-created_at')
    )

    now = timezone.now()
    past_appointments = []

    for app in all_appointments:
        if get_appointment_end(app) <= now:
            past_appointments.append(app)

    return render(request, 'appointments/appointment_history.html', {
        'appointments': past_appointments,
    })
