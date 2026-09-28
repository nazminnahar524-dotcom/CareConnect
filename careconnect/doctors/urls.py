

from django.urls import path
from .views import doctor_list_view, doctor_detail_view

urlpatterns = [
    path('', doctor_list_view, name='doctor_list'),
    path('<int:pk>/', doctor_detail_view, name='doctor_detail'),
]