from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
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

    # -----------------------------
    # SEARCH
    # -----------------------------

    if search:
        pharmacies = (
            pharmacies.filter(name__icontains=search)
            | pharmacies.filter(address__icontains=search)
            | pharmacies.filter(area__icontains=search)
        )

    # -----------------------------
    # DISTRICT
    # -----------------------------

    if district:
        pharmacies = pharmacies.filter(
            district=district
        )

    # -----------------------------
    # SERVICES / FILTERS
    # -----------------------------

    if verified == "1":
        pharmacies = pharmacies.filter(
            verified=True
        )

    if emergency == "1":
        pharmacies = pharmacies.filter(
            emergency=True
        )

    if home_delivery == "1":
        pharmacies = pharmacies.filter(
            home_delivery=True
        )

    if online_order == "1":
        pharmacies = pharmacies.filter(
            online_order=True
        )

    # -----------------------------
    # DISTRICT LIST
    # -----------------------------

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


# ============================================================
# DISTANCE CALCULATION
# ============================================================

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates
    using the Haversine formula.

    Returns distance in meters.
    """

    earth_radius = 6371000

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

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius * c


# ============================================================
# NEARBY PHARMACIES
# ============================================================

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

        latitude = float(
            request.POST.get("latitude")
        )

        longitude = float(
            request.POST.get("longitude")
        )

        radius = float(
            request.POST.get(
                "radius",
                2000
            )
        )

    except (TypeError, ValueError):

        return JsonResponse(
            {
                "success": False,
                "error": (
                    "Invalid latitude, longitude "
                    "or radius."
                )
            },
            status=400
        )

    # Maximum radius = 50 km
    radius = max(
        1,
        min(radius, 50000)
    )

    # Only pharmacies with coordinates
    pharmacies = Pharmacy.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    )

    results = []

    for pharmacy in pharmacies:

        try:

            pharmacy_latitude = float(
                pharmacy.latitude
            )

            pharmacy_longitude = float(
                pharmacy.longitude
            )

        except (TypeError, ValueError):

            continue

        distance = calculate_distance(
            latitude,
            longitude,
            pharmacy_latitude,
            pharmacy_longitude
        )

        if distance <= radius:

            results.append(
                {
                    "id": pharmacy.id,
                    "name": pharmacy.name,
                    "address": pharmacy.address,
                    "latitude": pharmacy_latitude,
                    "longitude": pharmacy_longitude,
                    "phone": pharmacy.phone or "",
                    "website": pharmacy.website or "",

                    "distance": round(distance),

                    "distance_km": round(
                        distance / 1000,
                        2
                    ),

                    "google_maps_url": (
                        "https://www.google.com/maps/dir/"
                        "?api=1"
                        f"&destination="
                        f"{pharmacy_latitude},"
                        f"{pharmacy_longitude}"
                    ),

                    "open_now": None,

                    "verified": pharmacy.verified,
                    "emergency": pharmacy.emergency,
                    "home_delivery": pharmacy.home_delivery,
                    "online_order": pharmacy.online_order,
                    "is_24_7": pharmacy.is_24_7,
                }
            )

    # Nearest first
    results.sort(
        key=lambda pharmacy: pharmacy["distance"]
    )

    return JsonResponse(
        {
            "success": True,
            "count": len(results),
            "radius": radius,
            "results": results
        }
    )


# ============================================================
# PHARMACY DETAIL / PROFILE
# ============================================================

def pharmacy_detail(request, pk):

    # Find selected pharmacy
    pharmacy = get_object_or_404(
        Pharmacy,
        pk=pk
    )

    # --------------------------------------------------------
    # USER LIVE LOCATION
    # --------------------------------------------------------

    user_latitude = request.GET.get("lat")
    user_longitude = request.GET.get("lng")

    distance_km = None

    if (
        user_latitude
        and user_longitude
        and pharmacy.latitude is not None
        and pharmacy.longitude is not None
    ):

        try:

            user_latitude = float(
                user_latitude
            )

            user_longitude = float(
                user_longitude
            )

            pharmacy_latitude = float(
                pharmacy.latitude
            )

            pharmacy_longitude = float(
                pharmacy.longitude
            )

            distance_meters = calculate_distance(
                user_latitude,
                user_longitude,
                pharmacy_latitude,
                pharmacy_longitude
            )

            distance_km = round(
                distance_meters / 1000,
                2
            )

        except (TypeError, ValueError):

            distance_km = None

    # --------------------------------------------------------
    # OPEN / CLOSED
    # --------------------------------------------------------

    is_open_now = None

    if pharmacy.is_24_7:

        is_open_now = True

    elif (
        pharmacy.opening_time
        and pharmacy.closing_time
    ):

        current_time = (
            timezone.localtime().time()
        )

        # Normal opening hours
        if pharmacy.opening_time <= pharmacy.closing_time:

            is_open_now = (
                pharmacy.opening_time
                <= current_time
                <= pharmacy.closing_time
            )

        # Overnight opening hours
        else:

            is_open_now = (
                current_time >= pharmacy.opening_time
                or
                current_time <= pharmacy.closing_time
            )

    # --------------------------------------------------------
    # GOOGLE MAPS DIRECTIONS
    # --------------------------------------------------------

    google_maps_url = None

    if (
        pharmacy.latitude is not None
        and pharmacy.longitude is not None
    ):

        google_maps_url = (
            "https://www.google.com/maps/dir/"
            "?api=1"
            f"&destination="
            f"{pharmacy.latitude},"
            f"{pharmacy.longitude}"
        )

    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    context = {
        "pharmacy": pharmacy,
        "distance_km": distance_km,
        "is_open_now": is_open_now,
        "google_maps_url": google_maps_url,
        "user_latitude": user_latitude,
        "user_longitude": user_longitude,
    }

    return render(
        request,
        "pharmacies/pharmacy_detail.html",
        context
    )