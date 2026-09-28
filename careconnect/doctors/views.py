from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import Doctor

def doctor_list_view(request):
    specialty = request.GET.get('specialty', '')
    query = request.GET.get('q', '')
    doctors = Doctor.objects.all()

    if specialty:
        doctors = doctors.filter(specialty__icontains=specialty)
    if query:
        doctors = doctors.filter(name__icontains=query) | doctors.filter(hospital_name__icontains=query)

    specialties = Doctor.objects.values_list('specialty', flat=True).distinct()

    context = {
        'doctors': doctors,
        'specialties': specialties,
        'selected_specialty': specialty,
        'query': query,
    }
    return render(request, 'doctors/doctor_list.html', context)

def doctor_detail_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})