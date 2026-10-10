from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Hospital


def hospital_list_view(request):
    """
    Renders the hospital listing page with filtering and network summary statistics.
    """
    query = request.GET.get('q', '')
    hospitals = Hospital.objects.all()

    if query:
        hospitals = hospitals.filter(name__icontains=query)

    # Calculate summary metrics for the dashboard widgets
    total_hospitals = hospitals.count()
    total_beds = hospitals.aggregate(Sum('available_beds'))['available_beds__sum'] or 0

    context = {
        'hospitals': hospitals,
        'total_hospitals': total_hospitals,
        'total_beds': total_beds,
        'query': query,
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