from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, unique=True)
    is_verified = models.BooleanField(default=False)
    total_purchases = models.IntegerField(default=0, help_text="Total number of items purchased")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"

    def increment_purchase(self):
        """Increment purchase count when user buys something"""
        self.total_purchases += 1
        self.save()


class OTP(models.Model):
    """Model to store OTP for user verification"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')
    phone_number = models.CharField(max_length=20)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)

    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'

    def __str__(self):
        return f"OTP for {self.user.username}"

    def is_valid(self):
        """Check if OTP is not expired and attempts are available"""
        return timezone.now() < self.expires_at and self.attempts < self.max_attempts and not self.is_verified

    @staticmethod
    def generate_otp():
        """Generate a 4-digit OTP"""
        return ''.join(random.choices(string.digits, k=4))


class PasswordResetToken(models.Model):
    """Model to store password reset tokens"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='password_reset')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Password reset token for {self.user.username}"

    def is_valid(self):
        """Check if token is not expired and not used"""
        return timezone.now() < self.expires_at and not self.is_used

    @staticmethod
    def generate_token():
        """Generate a random token for password reset"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=50))
