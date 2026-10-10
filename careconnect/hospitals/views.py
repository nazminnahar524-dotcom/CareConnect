from django.shortcuts import render, get_object_or_404
from .models import Hospital


def hospital_list_view(request):
    """
    Renders the hospital listing page with filtering support.
    """
    query = request.GET.get('q', '')
    hospitals = Hospital.objects.all()

    if query:
        hospitals = hospitals.filter(name__icontains=query)

    context = {
        'hospitals': hospitals,
        'total_count': hospitals.count(),
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