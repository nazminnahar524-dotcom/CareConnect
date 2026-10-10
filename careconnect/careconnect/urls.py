from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main Views
    path('', views.home_view, name='home'),
    path('doctors/', include('doctors.urls')),
    path('appointments/', include('appointments.urls')),  # <--- Add this back
    path('pharmacies/', include('pharmacies.urls')),
    path('donors/', include('donors.urls')),
    path('hospitals/', include('hospitals.urls')),

    # Auth Views
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]