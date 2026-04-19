from django import forms
from .models import RequestNewLaptop


class RequestNewLaptopForm(forms.Form):
    """Form for users to request new laptops"""

    LAPTOP_TYPE_CHOICES = [
        ('', 'Choose a category...'),
        ('Ultrabooks', 'Ultrabooks'),
        ('Gaming Laptops', 'Gaming Laptops'),
        ('2-in-1 Convertibles', '2-in-1 Convertibles'),
        ('Professional Workstations', 'Professional Workstations'),
        ('Chromebooks', 'Chromebooks'),
        ('Rugged Laptops', 'Rugged Laptops'),
    ]

    laptop_type = forms.ChoiceField(
        choices=LAPTOP_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'required': True
        }),
        label="Laptop Category",
        help_text="Select the type of laptop that best fits your needs",
        required=True
    )

    laptop_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'E.g., Dell XPS 13, HP Pavilion 15, MacBook Pro'
        }),
        help_text="E.g., 'Dell XPS 13', 'Gaming laptop under ₹80,000', 'MacBook Pro M3'"
    )

