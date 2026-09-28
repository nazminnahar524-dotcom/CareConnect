from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list_view, name='doctor_list'),
    path('doctor/<int:pk>/', views.doctor_detail_view, name='doctor_detail'),
]