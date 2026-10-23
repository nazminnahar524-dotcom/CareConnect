
from django.contrib import admin
from .models import BloodRequest


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        "blood_group",
        "hospital_name",
        "bags_needed",
        "needed_by",
        "status",
        "requester",
    )
    list_filter = ("blood_group", "status")
    search_fields = ("hospital_name", "location_address")
