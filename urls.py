from django.conf.urls import include
from django.urls import re_path
from .staff_firewall.views import StaffFirewall
from .router.feature_routers import SimpleRouter

router = SimpleRouter(trailing_slash=False)

router.register(
    r'fw',
    StaffFirewall,
    basename='fw',
    feature_name='staff_firewall.fw')


urlpatterns = [
    re_path(r'^firewall/', include(router.urls)),
]