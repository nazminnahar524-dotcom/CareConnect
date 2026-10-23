
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Medicine


def medicine_list(request):
    # Total active medicines before applying search and filters
    total_medicines = Medicine.objects.filter(
        is_active=True
    ).count()

    # Start with all active medicines
    medicines = Medicine.objects.filter(is_active=True)

    # Search by medicine name, brand, generic name, or manufacturer
    search_query = request.GET.get("q", "").strip()

    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query)
            | Q(brand_name__icontains=search_query)
            | Q(generic_name__icontains=search_query)
            | Q(manufacturer__icontains=search_query)
        )

    # Filter by category
    category = request.GET.get("category", "").strip()

    if category:
        medicines = medicines.filter(category=category)

    # Filter by prescription requirement
    prescription = request.GET.get("prescription", "").strip()

    if prescription == "required":
        medicines = medicines.filter(prescription_required=True)
    elif prescription == "otc":
        medicines = medicines.filter(prescription_required=False)

    # Count results after applying search and filters
    medicines_count = medicines.count()

    context = {
        "medicines": medicines,
        "total_medicines": total_medicines,
        "medicines_count": medicines_count,
        "search_query": search_query,
        "selected_category": category,
        "selected_prescription": prescription,
        "categories": Medicine.CATEGORY_CHOICES,
    }

    return render(
        request,
        "medicines/medicine_list.html",
        context,
    )


def medicine_detail(request, pk):
    medicine = get_object_or_404(
        Medicine,
        pk=pk,
        is_active=True,
    )

    return render(
        request,
        "medicines/medicine_detail.html",
        {"medicine": medicine},
    )
