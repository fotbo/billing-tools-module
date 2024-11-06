from . import views
from django.urls import path

urlpatterns = [
    path('public/vpn-notification', views.public_vpn_notification, name='vpn-notification'),
]
