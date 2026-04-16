from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import RequestNewLaptop
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
            request_obj = form.save(commit=False)
            request_obj.user = user
            request_obj.name = user_name
            request_obj.email = user_email
            request_obj.mobile_number = user_mobile
            request_obj.save()
            
            messages.success(request, 
                f'Your laptop request has been submitted successfully! The shop owner will contact you at {user_mobile} to discuss details.')
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


@login_required(login_url='accounts:login')
def my_requests(request):
    """Show user's laptop requests"""
    user_requests = RequestNewLaptop.objects.filter(user=request.user)
    
    return render(request, 'new_laptops/my_requests.html', {
        'requests': user_requests,
        'page_title': 'My Laptop Requests'
    })

