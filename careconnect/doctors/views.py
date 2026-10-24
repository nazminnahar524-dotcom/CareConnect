
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import Doctor


@login_required
def doctor_list_view(request):
    specialty = request.GET.get('specialty', '').strip()
    query = request.GET.get('q', '').strip()

    doctors = Doctor.objects.select_related(
        'hospital'
    ).all().order_by('name')

    if specialty:
        doctors = doctors.filter(
            specialty__icontains=specialty
        )

    if query:
        doctors = doctors.filter(
            Q(name__icontains=query) |
            Q(hospital__name__icontains=query) |
            Q(specialty__icontains=query)
        )

    specialties = (
        Doctor.objects
        .values_list('specialty', flat=True)
        .distinct()
        .order_by('specialty')
    )

    return render(request, 'doctors/doctor_list.html', {
        'doctors': doctors,
        'specialties': specialties,
        'selected_specialty': specialty,
        'query': query,
    })


@login_required
def doctor_detail_view(request, pk):
    doctor = get_object_or_404(
        Doctor.objects.select_related('hospital'),
        pk=pk
    )

    return render(
        request,
        'doctors/doctor_detail.html',
        {'doctor': doctor}
    )
