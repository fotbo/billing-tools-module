import logging
from typing import Dict

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from fleio.core.drf import StaffOnly, CustomPermissions

from .models import (FwStaff,
                     FwAction,
                     FwDirection,
                     FwProtocol,
                     FwInterface,
                     FwRegions)
from fleio.openstack.models.instance import Instance
from .serializers import FwStaffSerializer, FwStaffDetailSerializer
from .opnsense import rule_manager
from .perm.custom_permissions import perm


from .tasks import cleanup_firewall_rule

LOG = logging.getLogger(__name__)

perm.init_perm()


class StaffFirewall(viewsets.ModelViewSet):

    permission_classes = [CustomPermissions, StaffOnly, ]
    queryset = FwStaff.objects.all()

    def get_serializer_class(self) -> FwStaffDetailSerializer | FwStaffSerializer:
        if self.action in ['list', 'retrieve']:
            return FwStaffDetailSerializer
        return FwStaffSerializer

    def create(self, request, *args, **kwargs) -> Response:
        try:
            resp = super().create(request=request, *args, **kwargs)
            return resp
        except Exception as e:
            LOG.error(e)
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance: object) -> None:
        conf_by_region = FwRegions.objects.filter(
            name=instance.region
            ).first()
        if str(conf_by_region.device_type) == 'OPNsense':
            rule_manager.delete(conf=conf_by_region, instance=instance)
        instance.delete()


    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs) -> Response(Dict[str, any]):
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

    @action(detail=True, methods=['post'])
    def toggle_rule(self, request, pk):
        obj = get_object_or_404(FwStaff, pk=pk)
        conf = FwRegions.objects.filter(
            name=obj.region
            ).first()
        toggle_status = rule_manager.toogle(
            conf=conf,
            firewall_uuid=obj.firewall_uuid)
        FwStaff.objects.filter(pk=pk).update(
            enabled=toggle_status.get('enabled'))

        return Response({'enabled': toggle_status.get('enabled')})

    # @action(detail=False, methods=['post'])
    # def webhook(self, request):
    #     cleanup_firewall_rule()
    #     return Response({'ok': 'ok'})