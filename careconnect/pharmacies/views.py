from django.http import JsonResponse
from django.shortcuts import render
from math import radians, sin, cos, sqrt, atan2

from .models import Pharmacy


def pharmacy_list(request):
    pharmacies = Pharmacy.objects.all()

    search = request.GET.get("search", "").strip()
    district = request.GET.get("district", "").strip()
    verified = request.GET.get("verified")
    emergency = request.GET.get("emergency")
    home_delivery = request.GET.get("home_delivery")
    online_order = request.GET.get("online_order")

    if search:
        pharmacies = pharmacies.filter(
            name__icontains=search
        ) | pharmacies.filter(
            address__icontains=search
        ) | pharmacies.filter(
            area__icontains=search
        )

    if district:
        pharmacies = pharmacies.filter(district=district)

    if verified == "1":
        pharmacies = pharmacies.filter(verified=True)

    if emergency == "1":
        pharmacies = pharmacies.filter(emergency=True)

    if home_delivery == "1":
        pharmacies = pharmacies.filter(home_delivery=True)

    if online_order == "1":
        pharmacies = pharmacies.filter(online_order=True)

    districts = (
        Pharmacy.objects
        .values_list("district", flat=True)
        .distinct()
        .order_by("district")
    )

    context = {
        "pharmacies": pharmacies,
        "districts": districts,
        "search": search,
        "selected_district": district,
        "verified": verified,
        "emergency": emergency,
        "home_delivery": home_delivery,
        "online_order": online_order,
    }

    return render(
        request,
        "pharmacies/pharmacy_list.html",
        context
    )


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using
    the Haversine formula.

    Returns distance in meters.
    """

    earth_radius = 6371000  # meters

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


def nearby_pharmacies(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "POST request required."
            },
            status=405
        )

    try:
        latitude = float(request.POST.get("latitude"))
        longitude = float(request.POST.get("longitude"))
        radius = float(request.POST.get("radius", 2000))

    except (TypeError, ValueError):
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid latitude, longitude or radius."
            },
            status=400
        )

    # Maximum radius = 50 km
    radius = max(1, min(radius, 50000))

    # Get only pharmacies that have coordinates
    pharmacies = Pharmacy.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    )

    results = []

    for pharmacy in pharmacies:

        try:
            pharmacy_latitude = float(pharmacy.latitude)
            pharmacy_longitude = float(pharmacy.longitude)

        except (TypeError, ValueError):
            continue

        distance = calculate_distance(
            latitude,
            longitude,
            pharmacy_latitude,
            pharmacy_longitude
        )

        # Only include pharmacies inside requested radius
        if distance <= radius:

            results.append({
                "id": pharmacy.id,
                "name": pharmacy.name,
                "address": pharmacy.address,
                "latitude": pharmacy_latitude,
                "longitude": pharmacy_longitude,
                "phone": pharmacy.phone or "",
                "website": pharmacy.website or "",
                "distance": round(distance),
                "distance_km": round(distance / 1000, 2),
                "google_maps_url": (
                    f"https://www.google.com/maps/dir/?api=1"
                    f"&destination={pharmacy_latitude},"
                    f"{pharmacy_longitude}"
                ),
                "open_now": None,
                "verified": pharmacy.verified,
                "emergency": pharmacy.emergency,
                "home_delivery": pharmacy.home_delivery,
                "online_order": pharmacy.online_order,
                "is_24_7": pharmacy.is_24_7,
            })

    # Nearest pharmacy first
    results.sort(
        key=lambda pharmacy: pharmacy["distance"]
    )

    return JsonResponse({
        "success": True,
        "count": len(results),
        "radius": radius,
        "results": results
    })