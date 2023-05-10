from django.urls import path
from .views import transfer

urlpatterns = [
    path('transfer/', transfer, name='transfer'),
]
