from django import forms
from .models import DonationHistory, Donor


class DonorRegistrationForm(forms.ModelForm):
    latitude = forms.FloatField(
        label='Location latitude',
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'id_latitude'}),
    )
    longitude = forms.FloatField(
        label='Location longitude',
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'id_longitude'}),
    )

    class Meta:
        model = Donor
        fields = [
            'full_name', 'profile_photo', 'blood_group', 'gender', 'age',
            'district', 'upazila', 'area', 'phone_number',
            'whatsapp_number', 'email', 'occupation',
            'languages', 'about_me', 'is_available', 'latitude', 'longitude'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
            'upazila': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Upazila'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your area or full address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+880 17...'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+880 17...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Student, Engineer'}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bangla, English'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a brief line about yourself...'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial.setdefault('latitude', self.instance.latitude)
            self.initial.setdefault('longitude', self.instance.longitude)

    def clean_latitude(self):
        latitude = self.cleaned_data['latitude']
        if latitude is not None and not -90 <= latitude <= 90:
            raise forms.ValidationError('Enter a latitude between -90 and 90.')
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data['longitude']
        if longitude is not None and not -180 <= longitude <= 180:
            raise forms.ValidationError('Enter a longitude between -180 and 180.')
        return longitude

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        if latitude is None or longitude is None:
            self.add_error(
                'latitude',
                'Choose a location on the map or use your current location.',
            )
            self.add_error(
                'longitude',
                'Choose a location on the map or use your current location.',
            )
        return cleaned_data


class DonationHistoryForm(forms.ModelForm):
    class Meta:
        model = DonationHistory
        fields = ['date', 'blood_group', 'location', 'organization']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hospital, blood bank, or area',
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization (optional)',
            }),
        }