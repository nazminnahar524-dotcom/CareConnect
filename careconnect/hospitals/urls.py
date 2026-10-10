from django.urls import path
from . import views

urlpatterns = [
    # Main Hospital List Page (e.g. /hospitals/)
    path('', views.hospital_list_view, name='hospital_list'),

    # Hospital Detail Page (e.g. /hospitals/1/)
    path('<int:pk>/', views.hospital_detail_view, name='hospital_detail'),
]