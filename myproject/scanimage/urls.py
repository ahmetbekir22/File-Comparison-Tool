from django.urls import path
from . import views  # Import your views.py

urlpatterns = [
    path('', views.scan_image_upload_view, name='scan_image_upload_view'),
    # Other URL patterns for your project
]
