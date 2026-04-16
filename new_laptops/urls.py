from django.urls import path
from . import views

app_name = 'new_laptops'

urlpatterns = [
    path('request/', views.request_new_laptop, name='request_laptop'),
    path('my-requests/', views.my_requests, name='my_requests'),
]
