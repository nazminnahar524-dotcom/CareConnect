from django.urls import path
from . import views

urlpatterns = [
    path('nearby/', views.nearby_donors, name='nearby_donors'),
    path('register/', views.register_donor, name='register_donor'),
    path('<int:donor_id>/', views.donor_detail, name='donor_detail'),
]