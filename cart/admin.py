from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_price', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'user']
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'
    
    def get_total_price(self, obj):
        return f"₹{obj.get_total_price():.2f}"
    get_total_price.short_description = 'Total Price'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'quantity', 'price', 'get_subtotal', 'cart', 'added_at']
    list_filter = ['app_label', 'added_at', 'cart__user']
    search_fields = ['product_name', 'cart__user__username']
    readonly_fields = ['added_at', 'app_label', 'product_id', 'product_name']
    
    def get_subtotal(self, obj):
        return f"₹{obj.get_subtotal():.2f}"
    get_subtotal.short_description = 'Subtotal'
    
    fieldsets = (
        ('Cart Information', {'fields': ('cart',)}),
        ('Product Details', {'fields': ('app_label', 'product_id', 'product_name', 'price')}),
        ('Quantity', {'fields': ('quantity',)}),
        ('Timestamps', {'fields': ('added_at',)})
    )


class OrderItemInline(admin.TabularInline):
    """Inline display of order items within Order admin"""
    model = OrderItem
    extra = 0
    fields = ['product_name', 'product_price', 'quantity', 'get_subtotal']
    readonly_fields = ['product_name', 'product_price', 'quantity', 'get_subtotal']
    
    def get_subtotal(self, obj):
        return f"₹{obj.get_subtotal():.2f}"
    get_subtotal.short_description = 'Subtotal'
    
    def has_delete_permission(self, request):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'delivery_city', 'status', 'get_total_amount', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'delivery_city', 'created_at']
    search_fields = ['order_id', 'user__username', 'user__email', 'delivery_full_name', 'delivery_phone']
    readonly_fields = ['order_id', 'created_at', 'updated_at', 'user']
    
    fieldsets = (
        ('Order Information', {'fields': ('order_id', 'user', 'payment_method', 'status')}),
        ('Delivery Address', {
            'fields': (
                'delivery_full_name', 'delivery_phone', 'delivery_email',
                'delivery_street_address', 'delivery_apartment',
                'delivery_city', 'delivery_state', 'delivery_postal_code'
            )
        }),
        ('Pricing', {
            'fields': ('subtotal', 'tax', 'delivery_charges', 'total_amount'),
            'classes': ('wide',)
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'delivered_at')}),
    )
    
    inlines = [OrderItemInline]
    
    def get_total_amount(self, obj):
        return f"₹{obj.total_amount:.2f}"
    get_total_amount.short_description = 'Total Amount'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'quantity', 'product_price', 'get_subtotal', 'order', 'app_label']
    list_filter = ['app_label', 'order__created_at', 'order__status']
    search_fields = ['product_name', 'order__order_id', 'order__user__username']
    readonly_fields = ['order', 'app_label', 'product_id', 'product_name', 'product_price']
    
    def get_subtotal(self, obj):
        return f"₹{obj.get_subtotal():.2f}"
    get_subtotal.short_description = 'Subtotal'
    
    fieldsets = (
        ('Order Information', {'fields': ('order',)}),
        ('Product Details', {'fields': ('app_label', 'product_id', 'product_name', 'product_price')}),
        ('Quantity', {'fields': ('quantity',)}),
    )

