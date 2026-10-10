from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('hospitals/', views.hospital_list_view, name='hospital_list'),
]