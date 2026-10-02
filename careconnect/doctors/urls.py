from django.urls import path
from .views import doctor_detail_view, doctor_list_view

urlpatterns = [
    path('', doctor_list_view, name='doctor_list'),
    path('<int:pk>/', doctor_detail_view, name='doctor_detail'),
]
