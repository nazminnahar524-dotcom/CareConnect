
from django.urls import path
from . import views

app_name = "blood_requests"

urlpatterns = [
    path("", views.request_list, name="list"),
    path("create/", views.request_create, name="create"),
    path(
        "hospital-search/",
        views.hospital_search,
        name="hospital_search",
    ),
    path("<int:pk>/close/", views.request_close, name="close"),
]
