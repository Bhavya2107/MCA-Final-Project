from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re


class UserRegistrationForm(UserCreationForm):
    """Form for user registration with phone number"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number (e.g., +66812345678)',
            'type': 'tel',
            'autocomplete': 'tel'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'autocomplete': 'username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Basic phone number validation
        if not re.match(r'^\+?[\d\s\-()]+$', phone_number):
            raise ValidationError('Please enter a valid phone number.')
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        """
        Save user with security: never allow registration as superuser or staff
        """
        user = super().save(commit=False)
        # Ensure new users are NOT superuser or staff
        user.is_superuser = False
        user.is_staff = False
        if commit:
            user.save()
        return user


class OTPVerificationForm(forms.Form):
    """Form for OTP verification"""
    otp_code = forms.CharField(
        max_length=6,
        min_length=4,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'placeholder': '0000',
            'inputmode': 'numeric',
            'autocomplete': 'off',
            'maxlength': '6'
        })
    )

    def clean_otp_code(self):
        otp_code = self.cleaned_data.get('otp_code')
        if not otp_code.isdigit():
            raise ValidationError('OTP must contain only digits.')
        return otp_code


class LoginForm(forms.Form):
    """Form for user login"""
    username_or_email = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'current-password'
        })
    )


class ForgotPasswordForm(forms.Form):
    """Form for forgot password email verification"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registered email address',
            'autocomplete': 'email'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('This email is not registered.')
        return email


class ResetPasswordForm(forms.Form):
    """Form for resetting password"""
    password1 = forms.CharField(
        label='New Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')
        if password1 and len(password1) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        return cleaned_data
