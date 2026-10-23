
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from hospitals.models import Hospital
from .forms import BloodRequestForm
from .models import BloodRequest


def hospital_search(request):
    query = request.GET.get("q", "").strip()

    if len(query) < 2:
        return JsonResponse({"results": []})

    hospitals = Hospital.objects.filter(
        Q(name__icontains=query)
        | Q(address__icontains=query)
        | Q(location__icontains=query)
    ).order_by("name")[:10]

    results = []

    for hospital in hospitals:
        if hospital.latitude is None or hospital.longitude is None:
            continue

        if not (
            -90 <= hospital.latitude <= 90
            and -180 <= hospital.longitude <= 180
        ):
            continue

        results.append({
            "id": hospital.pk,
            "name": hospital.name,
            "address": hospital.address,
            "location": hospital.location,
            "latitude": hospital.latitude,
            "longitude": hospital.longitude,
        })

    return JsonResponse({"results": results})


def request_list(request):
    requests = BloodRequest.objects.filter(
        status="active",
        needed_by__gt=timezone.now(),
    ).select_related("requester")

    group = request.GET.get("blood_group", "")
    if group in dict(BloodRequest.BLOOD_GROUPS):
        requests = requests.filter(blood_group=group)

    search = request.GET.get("q", "").strip()
    if search:
        requests = requests.filter(
            Q(hospital_name__icontains=search)
            | Q(location_address__icontains=search)
        )

    return render(
        request,
        "blood_requests/request_list.html",
        {
            "requests": requests,
            "blood_groups": BloodRequest.BLOOD_GROUPS,
        },
    )


@login_required
def request_create(request):
    if request.method == "POST":
        form = BloodRequestForm(request.POST)

        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()

            return redirect("blood_requests:list")
    else:
        form = BloodRequestForm()

    return render(
        request,
        "blood_requests/request_form.html",
        {"form": form},
    )


@login_required
def request_close(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)

    if (
        blood_request.requester_id != request.user.pk
        and not request.user.is_staff
    ):
        return HttpResponseForbidden(
            "You cannot close another user's request."
        )

    if request.method != "POST":
        return redirect("blood_requests:list")

    blood_request.status = "closed"
    blood_request.save(update_fields=["status"])

    return redirect("blood_requests:list")
