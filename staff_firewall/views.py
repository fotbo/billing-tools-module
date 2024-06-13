import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import FwStaff, FwRegions
from .serializers import FwStaffSerializer, FwStaffDetailSerializer
from fleio.core.drf import StaffOnly
from .opnsense_api import Opnsense

LOG = logging.getLogger(__name__)


class StaffFirewall(viewsets.ModelViewSet):

    permission_classes = [StaffOnly, ]
    queryset = FwStaff.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return FwStaffDetailSerializer
        return FwStaffSerializer

    def perform_create(self, serializer):
        conf_by_region = FwRegions.objects.filter(
            name=serializer.validated_data.get('region')
            ).first()
        if str(conf_by_region.device_type) == 'OPNsence':
            opnsense = Opnsense(
                api_url=conf_by_region.api_url,
                api_key=conf_by_region.api_key,
                api_secret=conf_by_region.api_secret)
            firewall = opnsense.firewall.filter_controller
            firewall.add_rule(
                description='test',
                direction='out',
                interface='opt1')