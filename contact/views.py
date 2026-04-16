from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import ContactInfo, Inquiry


def contact_page(request):
    info = ContactInfo.objects.first()
    # allow pre-filling product via ?product=Product+Name from product detail pages
    initial = {}
    product_q = request.GET.get('product')
    if product_q:
        initial['product'] = product_q

    form = ContactForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        Inquiry.objects.create(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            message=data['message'],
            product=data.get('product', ''),
        )
        return redirect('contact:contact_page')
    return render(request, 'contact/contact.html', {'info': info, 'form': form})
