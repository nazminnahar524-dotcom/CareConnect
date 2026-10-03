from django.urls import path
from . import views

urlpatterns = [
    path('', views.pharmacy_list, name='pharmacy_list'),
    path('nearby/', views.nearby_pharmacies, name='nearby_pharmacies'),
]