from django import forms
from .models import Donor

class DonorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            'full_name', 'blood_group', 'gender', 'age',
            'district', 'upazila', 'area', 'phone_number',
            'whatsapp_number', 'email', 'occupation',
            'languages', 'about_me', 'is_available'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
            'upazila': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Upazila'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Dhanmondi, Dhaka'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+880 17...'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+880 17...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Student, Engineer'}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bangla, English'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a brief line about yourself...'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }