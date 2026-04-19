from django import forms
from .models import Order


class DeliveryAddressForm(forms.ModelForm):
    """Form for collecting delivery address information"""
    
    class Meta:
        model = Order
        fields = [
            'delivery_full_name',
            'delivery_phone',
            'delivery_email',
            'delivery_street_address',
            'delivery_apartment',
            'delivery_city',
            'delivery_state',
            'delivery_postal_code',
        ]
        widgets = {
            'delivery_full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
                'required': True,
            }),
            'delivery_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
                'type': 'tel',
                'required': True,
            }),
            'delivery_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
                'required': True,
            }),
            'delivery_street_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address',
                'required': True,
            }),
            'delivery_apartment': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apartment, suite, etc. (optional)',
                'required': False,
            }),
            'delivery_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City',
                'required': True,
            }),
            'delivery_state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State',
                'required': True,
            }),
            'delivery_postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal code',
                'required': True,
            }),
        }

    def clean_delivery_phone(self):
        """Validate phone number"""
        phone = self.cleaned_data.get('delivery_phone')
        if phone and not phone.replace('-', '').replace(' ', '').isdigit():
            raise forms.ValidationError('Please enter a valid phone number')
        if phone and len(phone.replace('-', '').replace(' ', '')) < 10:
            raise forms.ValidationError('Phone number must be at least 10 digits')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('delivery_city', '').lower().strip()
        
        # Store normalization for later use
        cleaned_data['delivery_city'] = city
        
        return cleaned_data
