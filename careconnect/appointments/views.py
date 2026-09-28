from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from doctors.models import Doctor
from .models import Appointment


@login_required
def book_appointment(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)

    if request.method == 'POST':
        date = request.POST.get('appointment_date')
        slot = request.POST.get('time_slot')

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            appointment_date=date,
            time_slot=slot,
            status='Confirmed'
        )
        messages.success(request, f'Appointment booked successfully with Dr. {doctor.name}!')
        return redirect('my_appointments')

    return render(request, 'appointments/book_appointment.html', {'doctor': doctor})


@login_required
def my_appointments_view(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date')
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})