from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import InquiryForm
from contact.models import Inquiry


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('-created_at')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'used_laptops/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = InquiryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        Inquiry.objects.create(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            message=data['message'],
            product=data.get('product', product.name),
        )
        return redirect('used_laptops:product_detail', slug=product.slug)

    specs_data = product.specs
    if isinstance(specs_data, str):
        import json
        try:
            specs_data = json.loads(specs_data)
        except Exception:
            specs_data = None

    return render(request, 'used_laptops/product_detail.html', {'product': product, 'form': form, 'specs_data': specs_data})
