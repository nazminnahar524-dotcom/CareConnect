from django.urls import path
from . import views


urlpatterns = [

    # Pharmacy list
    path(
        '',
        views.pharmacy_list,
        name='pharmacy_list'
    ),

    # Nearby pharmacies API
    path(
        'nearby/',
        views.nearby_pharmacies,
        name='nearby_pharmacies'
    ),

    # Pharmacy profile/details
    path(
        '<int:pk>/',
        views.pharmacy_detail,
        name='pharmacy_detail'
    ),
]