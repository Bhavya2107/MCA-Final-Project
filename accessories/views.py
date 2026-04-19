from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Min, Max
from datetime import timedelta
from django.utils import timezone
from .models import Product, Category
from .forms import InquiryForm
from contact.models import Inquiry


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(products__available=True).distinct()
    products = Product.objects.filter(available=True)
    
    # Get price range
    price_stats = products.aggregate(min_price=Min('price'), max_price=Max('price'))
    min_price = price_stats['min_price'] or 0
    max_price = price_stats['max_price'] or 0
    
    # Category filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Price range filter
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=float(price_min))
    if price_max:
        products = products.filter(price__lte=float(price_max))
    
    # Recently added filter (last 7 days)
    show_recent = request.GET.get('show_recent')
    if show_recent == 'on':
        seven_days_ago = timezone.now() - timedelta(days=7)
        products = products.filter(created_at__gte=seven_days_ago)
    
    # Sorting
    sort_by = request.GET.get('sort_by', '-created_at')
    if sort_by in ['price', '-price', '-created_at', 'name']:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('-created_at')
    
    return render(request, 'accessories/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'min_price': int(min_price) if min_price else 0,
        'max_price': int(max_price) if max_price else 0,
        'selected_price_min': price_min or int(min_price) if min_price else 0,
        'selected_price_max': price_max or int(max_price) if max_price else 0,
        'show_recent': show_recent == 'on',
        'sort_by': sort_by,
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
        return redirect('accessories:product_detail', slug=product.slug)
    return render(request, 'accessories/product_detail.html', {'product': product, 'form': form})
