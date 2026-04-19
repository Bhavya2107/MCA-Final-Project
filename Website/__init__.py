try:
	from django.contrib import admin
	admin.site.site_header = "COMPUTER & CCTV HUB Admin"
	admin.site.site_title = "COMPUTER & CCTV HUB Admin Portal"
	admin.site.index_title = "Dashboard"
except Exception:
	# Running outside Django context or before admin is ready; ignore
	pass
