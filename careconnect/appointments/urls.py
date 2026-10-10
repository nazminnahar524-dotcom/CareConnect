
from django.urls import path
from . import views

urlpatterns = [
    path(
        "book/<int:doctor_pk>/",
        views.book_appointment,
        name="book_appointment"
    ),
    path(
        "my-list/",
        views.my_appointments_view,
        name="my_appointments"
    ),
    path(
        "history/",
        views.appointment_history_view,
        name="appointment_history"
    ),
    path(
        "cancel/<int:appointment_id>/",
        views.cancel_appointment,
        name="cancel_appointment"
    ),
]
