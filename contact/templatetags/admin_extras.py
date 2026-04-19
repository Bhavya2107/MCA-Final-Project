from django import template
from django.apps import apps

register = template.Library()

@register.simple_tag
def get_admin_counts():
    """Return counts for key models used in the admin dashboard."""
    counts = {}
    try:
        RequestNewLaptop = apps.get_model('new_laptops', 'RequestNewLaptop')
        UsedProduct = apps.get_model('used_laptops', 'Product')
        AccProduct = apps.get_model('accessories', 'Product')
        Inquiry = apps.get_model('contact', 'Inquiry')
        counts['new_requests'] = RequestNewLaptop.objects.count()
        counts['used_products'] = UsedProduct.objects.count()
        counts['accessories'] = AccProduct.objects.count()
        counts['inquiries'] = Inquiry.objects.count()
    except Exception:
        # If apps not ready or models missing, return zeros
        counts = {'new_requests': 0, 'used_products': 0, 'accessories': 0, 'inquiries': 0}
    return counts
