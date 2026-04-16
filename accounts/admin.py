from django.contrib import admin
from .models import UserProfile, OTP, PasswordResetToken


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_verified', 'total_purchases', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username', 'phone_number', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Verification & Contact', {
            'fields': ('phone_number', 'is_verified')
        }),
        ('Purchase Information', {
            'fields': ('total_purchases',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_verified', 'attempts', 'created_at', 'expires_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username', 'phone_number')
    readonly_fields = ('otp_code', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_used', 'created_at', 'expires_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('token', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
