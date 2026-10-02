from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from doctors.models import Doctor
from .models import Appointment


@login_required
def book_appointment(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)

    if request.method == 'POST':
        date_text = request.POST.get('appointment_date', '').strip()
        slot = request.POST.get('time_slot', '').strip()

        try:
            appointment_date = datetime.strptime(date_text, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Please select a valid appointment date.')
            return render(request, 'appointments/book_appointment.html', {'doctor': doctor})

        if appointment_date < timezone.localdate():
            messages.error(request, 'You cannot book an appointment for a past date.')
            return render(request, 'appointments/book_appointment.html', {'doctor': doctor})

        if not slot:
            messages.error(request, 'Please select a time slot.')
            return render(request, 'appointments/book_appointment.html', {'doctor': doctor})

        already_booked = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            time_slot=slot,
        ).exclude(status='Cancelled').exists()

        if already_booked:
            messages.error(request, 'This time slot is already booked. Please choose another slot.')
            return render(request, 'appointments/book_appointment.html', {'doctor': doctor})

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            appointment_date=appointment_date,
            time_slot=slot,
            status='Confirmed',
        )
        messages.success(request, f'Appointment booked successfully with Dr. {doctor.name}.')
        return redirect('my_appointments')

    return render(request, 'appointments/book_appointment.html', {
        'doctor': doctor,
        'today': timezone.localdate().isoformat(),
    })


@login_required
def my_appointments_view(request):
    appointments = (
        Appointment.objects
        .filter(patient=request.user)
        .select_related('doctor')
        .order_by('-appointment_date', '-created_at')
    )
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})
