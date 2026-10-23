
from django import forms
from django.utils import timezone

from .models import BloodRequest


class BloodRequestForm(forms.ModelForm):
    needed_by = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={
                "type": "datetime-local",
                "class": "form-control",
            },
        ),
    )

    class Meta:
        model = BloodRequest
        fields = [
            "blood_group",
            "bags_needed",
            "patient_relation",
            "hospital_name",
            "location_address",
            "latitude",
            "longitude",
            "contact_number",
            "needed_by",
        ]

        widgets = {
            "blood_group": forms.Select(
                attrs={"class": "form-select"}
            ),
            "bags_needed": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "patient_relation": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "hospital_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Search and select a hospital below",
                    "readonly": True,
                }
            ),
            "location_address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Selected hospital address",
                    "readonly": True,
                }
            ),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "contact_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean(self):
        cleaned = super().clean()

        lat = cleaned.get("latitude")
        lng = cleaned.get("longitude")
        bags = cleaned.get("bags_needed")
        needed_by = cleaned.get("needed_by")

        if lat is not None and not -90 <= lat <= 90:
            self.add_error("latitude", "Invalid latitude.")

        if lng is not None and not -180 <= lng <= 180:
            self.add_error("longitude", "Invalid longitude.")

        if (lat is None) != (lng is None):
            self.add_error(
                "latitude",
                "Both latitude and longitude are required.",
            )

        if lat is None or lng is None:
            self.add_error(
                "hospital_name",
                "Please select a hospital from the search results.",
            )

        if not cleaned.get("hospital_name"):
            self.add_error(
                "hospital_name",
                "Please select a hospital.",
            )

        if not cleaned.get("location_address"):
            self.add_error(
                "location_address",
                "Hospital address is required.",
            )

        if bags is not None and bags < 1:
            self.add_error(
                "bags_needed",
                "At least one bag is required.",
            )

        if needed_by is not None and needed_by <= timezone.now():
            self.add_error(
                "needed_by",
                "Choose a future date and time.",
            )

        return cleaned
