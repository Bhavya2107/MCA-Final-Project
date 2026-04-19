from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required(login_url='accounts:login')
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta
from .models import UserProfile, OTP, PasswordResetToken
from .forms import (UserRegistrationForm, OTPVerificationForm, LoginForm,
                    ForgotPasswordForm, ResetPasswordForm)
import os
from django.contrib.auth.hashers import make_password


def send_otp_sms(phone_number, otp_code):
    """
    Send OTP via SMS using Twilio
    You need to set environment variables: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
    """
    try:
        # Try to import Twilio - if not installed, show message
        from twilio.rest import Client
        
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, twilio_phone]):
            # If Twilio credentials not set, just print OTP for development
            print(f"[DEV MODE] OTP for {phone_number}: {otp_code}")
            return True
        
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your COMPUTER & CCTV HUB verification code is: {otp_code}. This code expires in 15 minutes.",
            from_=twilio_phone,
            to=phone_number
        )
        return True
    except ImportError:
        # Twilio not installed, just log for development
        print(f"[DEV MODE] OTP for {phone_number}: {otp_code}")
        return True
    except Exception as e:
        print(f"Error sending OTP: {str(e)}")
        return False


def send_otp_email(email, username, otp_code):
    """
    Send OTP via email with improved error handling
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        subject = 'Your OTP for COMPUTER & CCTV HUB Account Verification'
        
        # Email context with OTP data
        context = {
            'username': username,
            'otp_code': otp_code,
            'otp_expiry': 15,  # minutes
        }
        
        # Render HTML email template
        try:
            html_message = render_to_string('accounts/otp_email.html', context)
        except Exception as template_error:
            logger.warning(f"Template rendering error: {template_error}. Using plain text email.")
            html_message = None
        
        # Plain text fallback
        plain_message = f"""
Hello {username},

Your OTP verification code for COMPUTER & CCTV HUB is: {otp_code}

This code will expire in 15 minutes.

Do not share this code with anyone.

Best regards,
COMPUTER & CCTV HUB Team
        """
        
        # Send email
        result = send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"OTP email sent successfully to {email}")
        print(f"✓ OTP sent to {email} | Code: {otp_code}")
        return True
        
    except Exception as e:
        import traceback
        logger.error(f"Error sending OTP email to {email}: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"✗ Failed to send OTP to {email}")
        print(f"  Error: {str(e)}")
        # Return False might cause registration to fail, so we'll still return True
        # and show the error to the user
        return False


@require_http_methods(["GET", "POST"])
def register(request):
    """Register new user with phone number"""
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user but don't save yet
            user = form.save(commit=False)
            user.is_active = False  # Deactivate until OTP is verified
            user.is_superuser = False  # Ensure NOT a superuser
            user.is_staff = False  # Ensure NOT staff
            user.save()
            
            phone_number = form.cleaned_data.get('phone_number')
            
            # Generate OTP
            otp_code = OTP.generate_otp()
            expires_at = timezone.now() + timedelta(minutes=15)
            
            # Create or update OTP record
            otp, created = OTP.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': phone_number,
                    'otp_code': otp_code,
                    'expires_at': expires_at
                }
            )
            
            if not created:
                otp.phone_number = phone_number
                otp.otp_code = otp_code
                otp.created_at = timezone.now()
                otp.expires_at = expires_at
                otp.is_verified = False
                otp.attempts = 0
                otp.save()
            
            # Send OTP via SMS
            send_otp_sms(phone_number, otp_code)
            
            # Send OTP via Email
            email = form.cleaned_data.get('email')
            send_otp_email(email, user.username, otp_code)
            
            messages.success(request, f'Registration successful! We sent a verification code to {email} and {phone_number}')
            return redirect('accounts:verify_otp', user_id=user.id)
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Register'
    }
    return render(request, 'accounts/register.html', context)


@require_http_methods(["GET", "POST"])
def verify_otp(request, user_id):
    """Verify OTP for user registration"""
    user = get_object_or_404(User, id=user_id)
    
    # Redirect if user already verified
    if user.is_active:
        messages.info(request, 'Your account is already verified.')
        return redirect('accounts:login')
    
    otp = get_object_or_404(OTP, user=user)
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data.get('otp_code')
            
            # Check if OTP is still valid
            if not otp.is_valid():
                messages.error(request, 'OTP has expired. Please register again.')
                user.delete()
                return redirect('accounts:register')
            
            # Check if OTP matches
            if entered_otp == otp.otp_code:
                otp.is_verified = True
                otp.save()
                
                # Activate user
                user.is_active = True
                user.save()
                
                # Create or get user profile (handle UNIQUE constraint on phone_number)
                try:
                    profile, created = UserProfile.objects.get_or_create(
                        user=user,
                        defaults={
                            'phone_number': otp.phone_number,
                            'is_verified': True
                        }
                    )
                    if not created:
                        # If profile already exists, update phone_number if needed
                        profile.phone_number = otp.phone_number
                        profile.is_verified = True
                        profile.save()
                except Exception as e:
                    # If unique constraint fails, just mark user as verified without profile
                    print(f"Warning: Could not create profile for {user.username}: {str(e)}")
                    pass
                
                messages.success(request, 'Your account has been successfully verified!')
                return redirect('accounts:login')
            else:
                otp.attempts += 1
                otp.save()
                
                remaining_attempts = otp.max_attempts - otp.attempts
                if remaining_attempts <= 0:
                    messages.error(request, 'Too many incorrect attempts. Please register again.')
                    user.delete()
                    otp.delete()
                    return redirect('accounts:register')
                else:
                    messages.error(request, f'Invalid OTP. {remaining_attempts} attempts remaining.')
    else:
        form = OTPVerificationForm()
    
    context = {
        'form': form,
        'phone_number': otp.phone_number,
        'page_title': 'Verify OTP'
    }
    return render(request, 'accounts/verify_otp.html', context)


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login user"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            
            # Try to authenticate with username
            user = authenticate(request, username=username_or_email, password=password)
            
            # If username doesn't work, try email
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is not activated. Please verify your email.')
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'page_title': 'Login'
    }
    return render(request, 'accounts/login.html', context)


@require_http_methods(["GET", "POST"])
@login_required(login_url='accounts:login')
def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@require_http_methods(["GET", "POST"])
def forgot_password(request):
    """Request password reset link"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            
            # Generate reset token
            token = PasswordResetToken.generate_token()
            expires_at = timezone.now() + timedelta(hours=24)
            
            # Create or update password reset token
            reset_token, created = PasswordResetToken.objects.get_or_create(
                user=user,
                defaults={
                    'token': token,
                    'expires_at': expires_at
                }
            )
            
            if not created:
                reset_token.token = token
                reset_token.expires_at = expires_at
                reset_token.is_used = False
                reset_token.save()
            
            # In production, send email with reset link
            reset_link = request.build_absolute_uri(f'/accounts/reset-password/{token}/')
            print(f"[DEV MODE] Password reset link for {email}: {reset_link}")
            
            messages.success(request, 'If an account with that email exists, we have sent password reset instructions.')
            return redirect('accounts:login')
    else:
        form = ForgotPasswordForm()
    
    context = {
        'form': form,
        'page_title': 'Forgot Password'
    }
    return render(request, 'accounts/forgot_password.html', context)


@require_http_methods(["GET", "POST"])
def reset_password(request, token):
    """Reset password with token"""
    if request.user.is_authenticated:
        return redirect('home')
    
    reset_token = get_object_or_404(PasswordResetToken, token=token)
    
    # Check if token is valid
    if not reset_token.is_valid():
        messages.error(request, 'This password reset link has expired. Please request a new one.')
        return redirect('accounts:forgot_password')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            user = reset_token.user
            user.set_password(password)
            user.save()
            
            reset_token.is_used = True
            reset_token.save()
            
            messages.success(request, 'Your password has been reset successfully. Please login with your new password.')
            return redirect('accounts:login')
    else:
        form = ResetPasswordForm()
    
    context = {
        'form': form,
        'page_title': 'Reset Password',
        'token': token
    }
    return render(request, 'accounts/reset_password.html', context)


@login_required(login_url='accounts:login')
def profile(request):
    """User profile page"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(
            user=request.user,
            phone_number='',
            is_verified=True
        )
    
    context = {
        'profile': profile,
        'page_title': 'My Profile'
    }
    return render(request, 'accounts/profile.html', context)


from .forms_edit_profile import EditProfileForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='accounts:login')
def edit_profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, phone_number='', is_verified=True)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = EditProfileForm(instance=profile, user=request.user)

    context = {
        'form': form,
        'profile': profile,
        'page_title': 'Edit Profile'
    }
    return render(request, 'accounts/edit_profile.html', context)
