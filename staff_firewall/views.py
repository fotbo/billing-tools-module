import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import FwStaff, FwAction, FwDirection, FwProtocol, FwInterface, FwRegions
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

    def create(self, request, *args, **kwargs):
        try:
            resp = super().create(request=request, *args, **kwargs)
            return resp
        except (Exception) as e:
            return Response({'error': str(e)})
    
    def perform_create(self, serializer):
        conf_by_region = FwRegions.objects.filter(
            name=serializer.validated_data.get('region')
            ).first()
        if str(conf_by_region.device_type) == 'OPNsense':
            opnsense = Opnsense(
                api_url=conf_by_region.api_url,
                api_key=conf_by_region.api_key,
                api_secret=conf_by_region.api_secret)
            firewall = opnsense.firewall.filter_controller
            firewall_uuid = firewall.add_rule(
                direction=serializer.validated_data.get('direction', None),
                interface=serializer.validated_data.get('interface', None),
                source_net=serializer.validated_data.get('source_ip', None),
                destination_net=serializer.validated_data.get('destination_ip', None),
                action=serializer.validated_data.get('action'),
                protocol=serializer.validated_data.get('protocol'),
                source_port=serializer.validated_data.get('source_port', 0),
                destination_port=serializer.validated_data.get('destination_port', 0),
                description=serializer.validated_data.get('description', 0)
                )
            serializer.validated_data['firewall_uuid'] = firewall_uuid.get('uuid')
        serializer.save()
    
    
    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        choices_info = {
            'action': [choice[0] for choice in FwAction.choices],
            'direction': [choice[0] for choice in FwDirection.choices],
            'protocol': [choice[0] for choice in FwProtocol.choices],
            'interface': [
                {'name': choice[1], 'value': choice[0]} for choice in FwInterface.choices if choice[0] is not None
                ],
            'regions': [region.name for region in FwRegions.objects.all()]
        }
        return Response(choices_info)