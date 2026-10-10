from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Q
from .models import Hospital


def hospital_list_view(request):
    """
    Renders the rich hospital directory with multi-facility filters, location filter,
    sorting options, and network metrics.
    """
    query = request.GET.get('q', '')
    location_filter = request.GET.get('location', '')
    sort_by = request.GET.get('sort', 'name')

    has_emergency = request.GET.get('emergency', '')
    has_icu = request.GET.get('icu', '')
    has_ambulance = request.GET.get('ambulance', '')
    has_pharmacy = request.GET.get('pharmacy', '')

    hospitals = Hospital.objects.all()

    # Search filter
    if query:
        hospitals = hospitals.filter(
            Q(name__icontains=query) | Q(location__icontains=query) | Q(address__icontains=query)
        )

    # Location filter
    if location_filter:
        hospitals = hospitals.filter(location__icontains=location_filter)

    # Boolean Facility filters
    if has_emergency == 'true':
        hospitals = hospitals.filter(has_emergency=True)
    if has_icu == 'true':
        hospitals = hospitals.filter(has_icu=True)
    if has_ambulance == 'true':
        hospitals = hospitals.filter(has_ambulance=True)
    if has_pharmacy == 'true':
        hospitals = hospitals.filter(has_pharmacy=True)

    # Sorting
    if sort_by == 'beds_desc':
        hospitals = hospitals.order_by('-total_beds')
    elif sort_by == 'doctors_desc':
        hospitals = hospitals.order_by('-total_doctors')
    elif sort_by == 'name_desc':
        hospitals = hospitals.order_by('-name')
    else:
        hospitals = hospitals.order_by('name')

    # Aggregates
    all_hospitals = Hospital.objects.all()
    total_hospitals = all_hospitals.count()
    total_beds = all_hospitals.aggregate(Sum('total_beds'))['total_beds__sum'] or 0
    total_doctors = all_hospitals.aggregate(Sum('total_doctors'))['total_doctors__sum'] or 0
    emergency_centers = all_hospitals.filter(has_emergency=True).count()

    # Extract unique locations for dropdown
    locations = Hospital.objects.values_list('location', flat=True).distinct()

    context = {
        'hospitals': hospitals,
        'results_count': hospitals.count(),
        'total_hospitals': total_hospitals,
        'total_beds': total_beds,
        'total_doctors': total_doctors,
        'emergency_centers': emergency_centers,
        'locations': locations,
        'query': query,
        'location_filter': location_filter,
        'sort_by': sort_by,
        'has_emergency': has_emergency,
        'has_icu': has_icu,
        'has_ambulance': has_ambulance,
        'has_pharmacy': has_pharmacy,
    }
    return render(request, 'hospitals/hospital_list.html', context)


def hospital_detail_view(request, pk):
    """
    Renders the detailed view for a single hospital.
    """
    hospital = get_object_or_404(Hospital, pk=pk)
    context = {
        'hospital': hospital,
    }
    return render(request, 'hospitals/hospital_detail.html', context)