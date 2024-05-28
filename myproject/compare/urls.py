from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_and_compare_files, name='upload_and_compare_files'),
    path('delete/', views.delete_files, name='delete_files'),
    path('generate_and_download_diff/', views.generate_and_download_diff, name='generate_and_download_diff'),


]
