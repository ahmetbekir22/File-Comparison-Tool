# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_upload_view, name='image_upload_view'),
]