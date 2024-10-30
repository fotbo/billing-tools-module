from django.conf.urls import include
from django.urls import re_path, path
from .staff_firewall.views import StaffFirewall
from .router.feature_routers import SimpleRouter

router = SimpleRouter(trailing_slash=False)

router.register(r'firewall', StaffFirewall, basename='staff_firewall', feature_name='tools.staff_firewall')
urlpatterns = [
    re_path(r'^tools/', include(router.urls)),
    path('fotbo/', include(('fleiostaff.tools.fotbo.urls', 'fotbo'), namespace='fotbo')),
]
