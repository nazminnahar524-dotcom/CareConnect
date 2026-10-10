from django.shortcuts import render


def dashboard_view(request):
    """
    Renders the main home dashboard page.
    """
    # Dynamic counts for dashboard stat cards
    context = {
        'total_hospitals': 2,
        'total_doctors': 0,
        'total_bookings': 0,
    }
    return render(request, 'hospitals/home_dashboard.html', context)


def hospital_list_view(request):
    """
    Renders the hospital listing page.
    """
    # Sample static data to display until database models are populated
    hospitals = [
        {
            'name': 'City General Hospital',
            'location': 'Dhaka',
            'contact': '+880 1700-000000',
            'available_beds': 12,
        },
        {
            'name': 'CareConnect Central Clinic',
            'location': 'Dhanmondi, Dhaka',
            'contact': '+880 1800-000000',
            'available_beds': 5,
        },
    ]
    context = {
        'hospitals': hospitals,
    }
    return render(request, 'hospitals/hospital_list.html', context)