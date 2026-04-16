from django import forms
from .models import RequestNewLaptop


class RequestNewLaptopForm(forms.ModelForm):
    """Form for users to request new laptops"""
    
    class Meta:
        model = RequestNewLaptop
        fields = ['laptop_type', 'laptop_name']
        widgets = {
            'laptop_type': forms.Select(attrs={
                'class': 'form-control form-control-lg',
                'required': True
            }),
            'laptop_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'E.g., Dell XPS 13, HP Pavilion 15, MacBook Pro',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['laptop_type'].label = "Laptop Type/Category"
        self.fields['laptop_name'].label = "Laptop Model/Name You Want"

