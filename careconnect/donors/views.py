import math
from urllib.parse import urlencode

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .models import DonationHistory, Donor
from .forms import DonationHistoryForm, DonorRegistrationForm


VIEWER_LATITUDE_SESSION_KEY = 'nearby_donor_viewer_latitude'
VIEWER_LONGITUDE_SESSION_KEY = 'nearby_donor_viewer_longitude'
VIEWER_LOCATION_LABEL_SESSION_KEY = 'nearby_donor_viewer_location_label'


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    a = min(1.0, max(0.0, a))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def nearby_donors(request):
    if request.method == 'POST':
        if request.POST.get('location_action') == 'clear':
            request.session.pop(VIEWER_LATITUDE_SESSION_KEY, None)
            request.session.pop(VIEWER_LONGITUDE_SESSION_KEY, None)
            request.session.pop(VIEWER_LOCATION_LABEL_SESSION_KEY, None)
        elif request.POST.get('location_action') == 'set':
            try:
                selected_latitude = float(request.POST.get('latitude', ''))
                selected_longitude = float(request.POST.get('longitude', ''))
                if (
                    not math.isfinite(selected_latitude)
                    or not math.isfinite(selected_longitude)
                    or not -90 <= selected_latitude <= 90
                    or not -180 <= selected_longitude <= 180
                ):
                    raise ValueError
            except ValueError:
                messages.error(
                    request,
                    'Could not use that location. Please try selecting it again.',
                )
            else:
                request.session[VIEWER_LATITUDE_SESSION_KEY] = selected_latitude
                request.session[VIEWER_LONGITUDE_SESSION_KEY] = selected_longitude
                location_label = request.POST.get('location_label', '').strip()
                request.session[VIEWER_LOCATION_LABEL_SESSION_KEY] = (
                    location_label[:120] or 'your current location'
                )

        filters = {
            key: request.POST.get(key, '')
            for key in ('blood_group', 'gender', 'address')
            if request.POST.get(key)
        }
        if request.POST.get('radius'):
            filters['radius'] = request.POST['radius']
        query_string = urlencode(filters)
        return redirect(
            f"{reverse('nearby_donors')}?{query_string}"
            if query_string else 'nearby_donors'
        )

    blood_group = request.GET.get('blood_group', '')
    gender = request.GET.get('gender', '')
    address = request.GET.get('address', '').strip()

    session_latitude = request.session.get(VIEWER_LATITUDE_SESSION_KEY)
    session_longitude = request.session.get(VIEWER_LONGITUDE_SESSION_KEY)
    query_has_location = 'lat' in request.GET or 'lng' in request.GET
    try:
        if query_has_location:
            user_lat = float(request.GET.get('lat', ''))
            user_lng = float(request.GET.get('lng', ''))
        elif session_latitude is not None and session_longitude is not None:
            user_lat = float(session_latitude)
            user_lng = float(session_longitude)
        else:
            raise ValueError
        if (
            not math.isfinite(user_lat)
            or not math.isfinite(user_lng)
            or not -90 <= user_lat <= 90
            or not -180 <= user_lng <= 180
        ):
            raise ValueError
        location_is_default = False
        if query_has_location or session_latitude is None:
            location_label = 'your current location'
        else:
            location_label = request.session.get(
                VIEWER_LOCATION_LABEL_SESSION_KEY,
                'your current location',
            )
    except ValueError:
        user_lat, user_lng = 23.7461, 90.3742
        location_is_default = True
        location_label = 'Dhanmondi, Dhaka'

    try:
        radius = float(request.GET.get('radius', 20050.0))
        if not math.isfinite(radius) or radius <= 0:
            raise ValueError
    except ValueError:
        radius = 20050.0

    donors = Donor.objects.filter(is_available=True)
    available_donors_count = donors.count()

    if blood_group and blood_group != 'All Groups':
        donors = donors.filter(blood_group=blood_group)
    if gender and gender != 'All':
        donors = donors.filter(gender=gender)
    if address:
        donors = donors.filter(
            Q(area__icontains=address)
            | Q(upazila__icontains=address)
            | Q(district__icontains=address)
        )

    donor_list = []
    for donor in donors:
        if donor.latitude is None or donor.longitude is None:
            donor.distance = None
            donor_list.append(donor)
            continue

        dist = calculate_distance(user_lat, user_lng, donor.latitude, donor.longitude)
        if dist <= radius:
            donor.distance = round(dist, 1)
            donor_list.append(donor)

    # Sort donors by nearest distance
    donor_list.sort(key=lambda x: (
        x.distance is None,
        x.distance if x.distance is not None else 0,
    ))

    context = {
        'donors': donor_list,
        'user_lat': user_lat,
        'user_lng': user_lng,
        'location_is_default': location_is_default,
        'location_label': location_label,
        'selected_radius': radius,
        'radius': radius,
        'total_donors': len(donor_list),
        'available_donors_count': available_donors_count,
        'selected_blood_group': blood_group,
        'selected_gender': gender,
        'selected_address': address,
    }
    return render(request, 'donors/nearby_donors.html', context)


def register_donor(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            donor = form.save(commit=False)
            if (
                request.user.is_authenticated
                and not Donor.objects.filter(user=request.user).exists()
            ):
                donor.user = request.user
            donor.save()
            messages.success(request, 'Thank you for registering as a blood donor!')
            return redirect('nearby_donors')
    else:
        form = DonorRegistrationForm()

    return render(request, 'donors/register_donor.html', {
        'form': form,
        'page_title': 'Register as a Blood Donor',
        'submit_label': 'Submit & Become a Donor',
    })


def edit_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST, request.FILES, instance=donor)
        if form.is_valid():
            donor = form.save()
            messages.success(request, 'Donor profile updated successfully.')
            if donor.is_available:
                return redirect('donor_detail', donor_id=donor.id)
            return redirect('nearby_donors')
    else:
        form = DonorRegistrationForm(instance=donor)

    return render(request, 'donors/register_donor.html', {
        'form': form,
        'page_title': 'Edit Donor Profile',
        'submit_label': 'Update Donor Profile',
        'donor': donor,
    })


def delete_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    if request.method == 'POST':
        donor_name = donor.full_name
        donor.delete()
        messages.success(request, f'{donor_name}\'s donor profile was deleted.')
        return redirect('nearby_donors')

    return render(request, 'donors/confirm_delete.html', {'donor': donor})


def donor_detail(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id, is_available=True)
    donation_history = donor.donation_history.order_by('-date', '-id')
    context = {
        'donor': donor,
        'donation_history': donation_history,
    }
    return render(request, 'donors/donor_detail.html', context)


def donor_donation_history(request, donor_id, history_id=None):
    donor = get_object_or_404(Donor, id=donor_id, is_available=True)
    history = None
    if history_id is not None:
        history = get_object_or_404(
            DonationHistory,
            id=history_id,
            donor=donor,
        )

    if request.method == 'POST':
        form = DonationHistoryForm(request.POST, instance=history)
        if form.is_valid():
            donation_history = form.save(commit=False)
            donation_history.donor = donor
            donation_history.save()
            latest_donation_date = donor.donation_history.order_by(
                '-date'
            ).values_list('date', flat=True).first()
            if donor.last_donated != latest_donation_date:
                donor.last_donated = latest_donation_date
                donor.save(update_fields=['last_donated'])
            action = 'updated' if history else 'added'
            messages.success(request, f'Donation history {action} successfully.')
            return redirect('donor_detail', donor_id=donor.id)
    else:
        form = DonationHistoryForm(instance=history)

    return render(request, 'donors/donation_history_form.html', {
        'donor': donor,
        'form': form,
        'history': history,
    })