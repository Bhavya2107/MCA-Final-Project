from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging
from .models import RequestNewLaptop, LaptopCategory
from .forms import RequestNewLaptopForm


@require_http_methods(["GET", "POST"])
@login_required(login_url='accounts:login')
def request_new_laptop(request):
    """Allow users to request new laptops instead of direct purchase"""

    # Get user info for auto-fill
    user = request.user
    user_email = user.email
    user_name = f"{user.first_name} {user.last_name}".strip() if user.first_name or user.last_name else user.username
    user_mobile = ''

    try:
        user_mobile = user.profile.phone_number
    except:
        user_mobile = ''

    if request.method == 'POST':
        form = RequestNewLaptopForm(request.POST)
        if form.is_valid():
            # Get or create the laptop category
            laptop_type_name = form.cleaned_data.get('laptop_type')
            laptop_category, created = LaptopCategory.objects.get_or_create(
                name=laptop_type_name
            )

            request_obj = RequestNewLaptop(
                user=user,
                name=user_name,
                email=user_email,
                mobile_number=user_mobile,
                laptop_type=laptop_category,
                laptop_name=form.cleaned_data.get('laptop_name')
            )
            request_obj.save()

            send_laptop_request_notifications(request_obj)

            messages.success(request,
                'Your laptop request has been submitted successfully! You will receive a confirmation email shortly.')
            return redirect('new_laptops:my_requests')
    else:
        form = RequestNewLaptopForm()

    return render(request, 'new_laptops/request_laptop.html', {
        'form': form,
        'page_title': 'Request a Laptop',
        'user_name': user_name,
        'user_email': user_email,
        'user_mobile': user_mobile,
    })


def send_laptop_request_notifications(request_obj):
    logger = logging.getLogger(__name__)
    host_email = getattr(settings, 'NEW_LAPTOP_REQUEST_NOTIFICATION_EMAIL', settings.EMAIL_HOST_USER)

    context = {
        'request': request_obj,
        'site_name': 'COMPUTER & CCTV HUB',
    }

    user_subject = 'Laptop Request Submitted - COMPUTER & CCTV HUB'
    try:
        user_html = render_to_string('new_laptops/email/new_laptop_request_user.html', context)
    except Exception as e:
        logger.warning(f'Could not render user email template: {e}')
        user_html = None

    user_plain = (
        f'Thank you {request_obj.name},\n\n'
        'Your laptop request has been submitted successfully. Our team will review it and contact you soon.\n\n'
        'Request Summary:\n'
        f'- Email: {request_obj.email}\n'
        f'- Mobile: {request_obj.mobile_number}\n'
        f'- Laptop Category: {request_obj.laptop_type}\n'
        f'- Laptop Model / Requirements: {request_obj.laptop_name}\n\n'
        'Thank you for choosing COMPUTER & CCTV HUB.'
    )

    if request_obj.email:
        try:
            send_mail(
                subject=user_subject,
                message=user_plain,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request_obj.email],
                html_message=user_html,
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f'Error sending user notification email to {request_obj.email}: {e}')
    else:
        logger.warning('Request user email is empty; skipping user notification email.')

    host_subject = f'[Laptop Request] New request from {request_obj.name}'
    try:
        host_html = render_to_string('new_laptops/email/new_laptop_request_host.html', context)
    except Exception as e:
        logger.warning(f'Could not render host email template: {e}')
        host_html = None

    host_plain = (
        'A new laptop request has been submitted.\n\n'
        'Request Details:\n'
        f'- Name: {request_obj.name}\n'
        f'- Email: {request_obj.email}\n'
        f'- Mobile Number: {request_obj.mobile_number}\n'
        f'- Laptop Category: {request_obj.laptop_type}\n'
        f'- Laptop Model / Requirements: {request_obj.laptop_name}\n'
        f'- Submitted at: {request_obj.created_at.strftime("%Y-%m-%d %H:%M %Z") if request_obj.created_at else "N/A"}\n\n'
        'Please review the request in the admin panel and contact the user as soon as possible.'
    )

    try:
        send_mail(
            subject=host_subject,
            message=host_plain,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[host_email],
            html_message=host_html,
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f'Error sending host notification email to {host_email}: {e}')


@login_required(login_url='accounts:login')
def my_requests(request):
    """Show user's laptop requests"""
    user_requests = RequestNewLaptop.objects.filter(user=request.user)
    
    return render(request, 'new_laptops/my_requests.html', {
        'requests': user_requests,
        'page_title': 'My Laptop Requests'
    })

