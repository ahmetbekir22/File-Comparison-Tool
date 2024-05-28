# character_counter/urls.py

from django.urls import path
from .views import character_counter

urlpatterns = [
    path('', character_counter, name='character_counter'),
]
