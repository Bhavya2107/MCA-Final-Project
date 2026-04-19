from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class LaptopCategory(models.Model):
    """Laptop categories for inquiry requests"""
    name = models.CharField(max_length=120)
    
    class Meta:
        verbose_name_plural = 'Laptop Categories'

    def __str__(self):
        return self.name


class RequestNewLaptop(models.Model):
    """Model to store laptop purchase requests from users"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Owner Contacted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='laptop_requests')
    name = models.CharField(max_length=200, default='')
    email = models.EmailField(default='')
    mobile_number = models.CharField(max_length=20, default='')
    laptop_type = models.ForeignKey(LaptopCategory, on_delete=models.SET_NULL, null=True, blank=False)
    laptop_name = models.CharField(max_length=200, help_text="Laptop model/name you want")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    owner_notes = models.TextField(blank=True, help_text="Notes from shop owner")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contacted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'New Laptop Requests'

    def __str__(self):
        return f"Request from {self.user.username} - {self.laptop_name}"

    def mark_as_contacted(self):
        """Mark request as contacted by owner"""
        if self.status == 'pending':
            self.status = 'contacted'
            self.contacted_at = timezone.now()
            self.save()

