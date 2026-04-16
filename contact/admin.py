from django.contrib import admin
from .models import Inquiry, ContactInfo


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'product', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('name', 'email', 'product')
    list_filter = ('created_at',)
    actions = ('export_as_csv',)

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        meta = self.model._meta
        field_names = ['name', 'email', 'phone', 'product', 'message', 'created_at']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=inquiries.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = [getattr(obj, f) for f in field_names]
            writer.writerow(row)
        return response

    export_as_csv.short_description = "Export selected inquiries as CSV"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'phone', 'email')
    search_fields = ('business_name', 'email', 'phone')
    readonly_fields = ()
