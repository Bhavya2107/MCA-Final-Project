from django.contrib import admin
from .models import LaptopCategory, RequestNewLaptop


@admin.register(LaptopCategory)
class LaptopCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(RequestNewLaptop)
class RequestNewLaptopAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'laptop_name', 'laptop_type', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'laptop_type')
    search_fields = ('user__username', 'name', 'email', 'laptop_name')
    readonly_fields = ('created_at', 'updated_at', 'contacted_at', 'user')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'name', 'email', 'mobile_number')
        }),
        ('Request Details', {
            'fields': ('laptop_type', 'laptop_name')
        }),
        ('Status & Response', {
            'fields': ('status', 'owner_notes', 'contacted_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ('mark_as_contacted', 'mark_as_in_progress', 'mark_as_completed', 'mark_as_rejected')

    def mark_as_contacted(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='contacted')
        self.message_user(request, f"{updated} request(s) marked as contacted")

    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f"{updated} request(s) marked as in progress")

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} request(s) marked as completed")

    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} request(s) marked as rejected")

    mark_as_contacted.short_description = "Mark selected requests as contacted"
    mark_as_in_progress.short_description = "Mark selected requests as in progress"
    mark_as_completed.short_description = "Mark selected requests as completed"
    mark_as_rejected.short_description = "Mark selected requests as rejected"

