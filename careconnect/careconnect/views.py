from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from doctors.models import Doctor
from appointments.models import Appointment


@login_required
def home_view(request):
    """Main CareConnect dashboard. Users see it only after logging in."""
    doctors_count = Doctor.objects.count()
    appointments_count = Appointment.objects.filter(patient=request.user).count()
    upcoming_appointments = (
        Appointment.objects
        .filter(patient=request.user, appointment_date__gte=timezone.localdate())
        .exclude(status='Cancelled')
        .select_related('doctor')
        .order_by('appointment_date', 'created_at')[:3]
    )

    context = {
        'doctors_count': doctors_count,
        'appointments_count': appointments_count,
        'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'home.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in to continue.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    """Custom login view so an already authenticated user is never shown the login screen."""
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.POST.get('next') or request.GET.get('next')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(next_url or 'home')
    else:
        form = AuthenticationForm(request)

    return render(request, 'registration/login.html', {'form': form, 'next': next_url})
