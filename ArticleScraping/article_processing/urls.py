from django.urls import path
from .views import extract_data

urlpatterns = [
    path('extract/', extract_data, name='extract_data'),
]
