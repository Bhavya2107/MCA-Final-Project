from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px;border-radius:4px;" />', obj.image.url)
        return "-"

    preview.short_description = 'Preview'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'category', 'created_at')
    list_editable = ('available',)
    list_filter = ('available', 'category')
    search_fields = ('name', 'description', 'condition_notes')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    readonly_fields = ('created_at',)
    actions = ('make_available', 'make_unavailable')

    def make_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f"{updated} product(s) marked as available")

    def make_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f"{updated} product(s) marked as unavailable")

    make_available.short_description = "Mark selected products as available"
    make_unavailable.short_description = "Mark selected products as unavailable"
