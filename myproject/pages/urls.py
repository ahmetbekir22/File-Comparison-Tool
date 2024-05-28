from django.urls import path
from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('compare/', include('compare.urls')),
    path('image/', include('image.urls')),
    path('scanimage/', include('scanimage.urls')),

    # path('delete/', views.delete_files, name='delete_files'),
    # path('delete/', views.delete_files, name='delete_files'),
]


