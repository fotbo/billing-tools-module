from . import views
from django.urls import path

urlpatterns = [
    path('public/', views.public_view, name='ovpn'),
]
