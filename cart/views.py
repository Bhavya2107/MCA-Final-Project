from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from django.urls import reverse
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal, ROUND_HALF_UP
import uuid
from .models import Cart, CartItem, Order, OrderItem
from .forms import DeliveryAddressForm


def _get_product(app_label, pk):
    """Get product from any app"""
    try:
        Model = apps.get_model(app_label, 'Product')
        return Model.objects.get(pk=pk)
    except Exception:
        raise Http404('Product not found')


def _get_or_create_cart(user):
    """Get or create cart for authenticated user"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def calculate_delivery_charges(city):
    """
    Calculate delivery charges based on city
    Free delivery for Ahmedabad, ₹100 for other cities
    """
    city_normalized = city.lower().strip()
    if city_normalized == 'ahmedabad':
        return Decimal('0.00')
    else:
        return Decimal('100.00')


@login_required(login_url='accounts:login')
def add_to_cart(request, app_label, pk):
    """Add product to authenticated user's cart"""
    if request.method != 'POST':
        return redirect('/')
    
    product = _get_product(app_label, int(pk))
    cart = _get_or_create_cart(request.user)
    
    # Check if product already in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, app_label=app_label, product_id=pk)
        cart_item.increase_quantity()
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            cart=cart,
            app_label=app_label,
            product_id=pk,
            product_name=product.name,
            price=product.price,
            quantity=1
        )
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'cart:view'))


@login_required(login_url='accounts:login')
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product_name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('cart:view')


@login_required(login_url='accounts:login')
def update_cart_quantity(request, item_id):
    """Update quantity of item in cart"""
    if request.method != 'POST':
        return redirect('cart:view')
    
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Get available stock for validation
    try:
        Model = apps.get_model(cart_item.app_label, 'Product')
        product = Model.objects.get(pk=cart_item.product_id)
        if hasattr(product, 'stock'):
            available_stock = product.stock
        elif hasattr(product, 'available_stock'):
            available_stock = product.available_stock
        else:
            available_stock = 999
    except Exception:
        available_stock = 999
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, 'Item removed from cart!')
    elif quantity > available_stock:
        messages.error(request, f'Cannot add more than {available_stock} items. Only {available_stock} available in stock.')
    elif quantity >= 1:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated!')
    
    return redirect('cart:view')


@login_required(login_url='accounts:login')
def view_cart(request):
    """View authenticated user's cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
        
        # Get available stock for each item
        for item in items:
            try:
                Model = apps.get_model(item.app_label, 'Product')
                product = Model.objects.get(pk=item.product_id)
                # Handle different stock field names across apps
                if hasattr(product, 'stock'):
                    item.available_stock = product.stock
                elif hasattr(product, 'available_stock'):
                    item.available_stock = product.available_stock
                else:
                    # For apps without stock field (like used_laptops), assume unlimited
                    item.available_stock = 999
            except Exception:
                item.available_stock = 999  # Default fallback
        
    except Cart.DoesNotExist:
        cart = None
        items = []
    
    # Calculate totals
    subtotal = sum(Decimal(item.get_subtotal()) for item in items) if items else Decimal('0.00')
    TAX_RATE = Decimal('0.18')  # 18% GST
    tax = (subtotal * TAX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'page_title': 'Shopping Cart',
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='accounts:login')
def checkout(request):
    """
    Checkout page - show cart summary and button to proceed to delivery address
    """
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart:view')
    
    if not items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('cart:view')
    
    # Calculate totals
    subtotal = sum(Decimal(item.get_subtotal()) for item in items)
    TAX_RATE = Decimal('0.18')
    tax = (subtotal * TAX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'payment_method': 'Cash on Delivery (COD)',
        'page_title': 'Checkout',
    }
    return render(request, 'cart/checkout.html', context)


@login_required(login_url='accounts:login')
def delivery_address(request):
    """
    Collect delivery address from user
    Show different delivery charges based on city
    """
    # Ensure cart has items
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart:view')
    
    if not items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('cart:view')
    
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            # Calculate delivery charges based on city
            city = form.cleaned_data.get('delivery_city')
            delivery_charges = calculate_delivery_charges(city)
            
            # Calculate totals
            subtotal = sum(Decimal(item.get_subtotal()) for item in items)
            TAX_RATE = Decimal('0.18')
            tax = (subtotal * TAX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total_amount = (subtotal + tax + delivery_charges).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Create order
            order_id = f"LS-{uuid.uuid4().hex[:10].upper()}"
            order = Order.objects.create(
                order_id=order_id,
                user=request.user,
                payment_method='cod',
                status='pending',
                delivery_full_name=form.cleaned_data.get('delivery_full_name'),
                delivery_phone=form.cleaned_data.get('delivery_phone'),
                delivery_email=form.cleaned_data.get('delivery_email'),
                delivery_street_address=form.cleaned_data.get('delivery_street_address'),
                delivery_apartment=form.cleaned_data.get('delivery_apartment', ''),
                delivery_city=city,
                delivery_state=form.cleaned_data.get('delivery_state'),
                delivery_postal_code=form.cleaned_data.get('delivery_postal_code'),
                subtotal=subtotal,
                tax=tax,
                delivery_charges=delivery_charges,
                total_amount=total_amount,
            )
            
            # Create order items from cart items
            for cart_item in items:
                OrderItem.objects.create(
                    order=order,
                    app_label=cart_item.app_label,
                    product_id=cart_item.product_id,
                    product_name=cart_item.product_name,
                    product_price=cart_item.price,
                    quantity=cart_item.quantity,
                )
            
            # Clear cart
            cart.clear_cart()
            
            messages.success(request, f'Order placed successfully! Order ID: {order_id}')
            return redirect('cart:order_confirmation', order_id=order_id)
    else:
        # Pre-populate form with user info
        initial_data = {
            'delivery_full_name': request.user.get_full_name() or request.user.username,
            'delivery_email': request.user.email,
        }
        
        # Try to get phone from user profile
        try:
            if hasattr(request.user, 'profile'):
                initial_data['delivery_phone'] = request.user.profile.phone_number
        except:
            pass
        
        form = DeliveryAddressForm(initial=initial_data)
    
    # Calculate current totals
    subtotal = sum(Decimal(item.get_subtotal()) for item in items)
    TAX_RATE = Decimal('0.18')
    tax = (subtotal * TAX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    context = {
        'form': form,
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'page_title': 'Delivery Address',
    }
    return render(request, 'cart/delivery_address.html', context)


@login_required(login_url='accounts:login')
def order_confirmation(request, order_id):
    """
    Show order confirmation page
    """
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
        'page_title': 'Order Confirmation',
    }
    return render(request, 'cart/order_confirmation.html', context)


@login_required(login_url='accounts:login')
def get_cart_count(request):
    """Get cart item count for AJAX"""
    try:
        cart = Cart.objects.get(user=request.user)
        count = cart.get_total_items()
    except Cart.DoesNotExist:
        count = 0
    
    return JsonResponse({'count': count})
    
    return JsonResponse({'count': count})

