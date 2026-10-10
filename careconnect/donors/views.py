from django.shortcuts import render, get_object_or_404, redirect
from .models import Donor
from .forms import DonorRegistrationForm


def nearby_donors(request):
    donors = Donor.objects.all()

    # Filter Logic
    blood_group = request.GET.get('blood_group')
    gender = request.GET.get('gender')

    if blood_group:
        donors = donors.filter(blood_group=blood_group)
    if gender and gender != 'All':
        donors = donors.filter(gender=gender)

    context = {
        'donors': donors,
        'available_donors_count': donors.filter(is_available=True).count()
    }
    return render(request, 'donors/nearby_donors.html', context)


def donor_detail(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    histories = donor.donation_histories.all()

    context = {
        'donor': donor,
        'histories': histories
    }
    return render(request, 'donors/donor_detail.html', context)


def register_donor(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            donor = form.save()
            return redirect('donor_detail', donor_id=donor.id)
    else:
        form = DonorRegistrationForm()

    return render(request, 'donors/register_donor.html', {'form': form})