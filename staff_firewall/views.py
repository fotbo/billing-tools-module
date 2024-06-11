import logging

from rest_framework import viewsets

from .models import FwStaff, FwRegions
from .serializers import FwStaffSerializer, FwStaffDetailSerializer
from fleio.core.drf import StaffOnly

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
            print(serializer.validated_data.get('action'))