from django.contrib import admin

# Customize admin site titles and headers
admin.site.site_header = "COMPUTER & CCTV HUB Admin"
admin.site.site_title = "COMPUTER & CCTV HUB Admin Panel"
admin.site.index_title = "Welcome to Admin Panel"

# Create language-specific versions
class ThaiAdminSite(admin.AdminSite):
    site_header = "ระบบจัดการ Laptop Shop"
    site_title = "แผงควบคุม Laptop Shop"
    index_title = "ยินดีต้อนรับเข้าสู่แผงควบคุม"

# You can use this custom admin site if you want Thai-only admin
# thai_admin_site = ThaiAdminSite(name='thai_admin')
