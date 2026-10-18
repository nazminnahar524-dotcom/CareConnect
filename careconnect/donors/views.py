import math
from django.shortcuts import render
from .models import Donor


def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance in km
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def nearby_donors(request):
    blood_group = request.GET.get('blood_group', '')
    gender = request.GET.get('gender', '')

    # Default location: Dhanmondi, Dhaka
    user_lat = float(request.GET.get('lat', 23.7461))
    user_lng = float(request.GET.get('lng', 90.3742))
    radius = float(request.GET.get('radius', 10.0))  # Default 10 km

    donors = Donor.objects.filter(is_available=True)

    if blood_group and blood_group != 'All Groups':
        donors = donors.filter(blood_group=blood_group)
    if gender and gender != 'All':
        donors = donors.filter(gender=gender)

    donor_list = []
    for donor in donors:
        # Distance calculation
        dist = calculate_distance(user_lat, user_lng, donor.latitude, donor.longitude)
        if dist <= radius:
            donor.distance = round(dist, 1)
            donor_list.append(donor)

    context = {
        'donors': donor_list,
        'user_lat': user_lat,
        'user_lng': user_lng,
        'radius': radius,
        'total_donors': len(donor_list),
        'selected_blood_group': blood_group,
        'selected_gender': gender,
    }
    return render(request, 'donors/nearby_donors.html', context)