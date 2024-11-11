from rest_framework import permissions
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from fleio.openstack.models import Instance, InstanceIPTracker
from plugins.tickets.enduser.tickets.serializers import TicketCreateSerializer
from fleio.core.models import AppUser, Client
from datetime import datetime, timedelta, timezone
from fleio.openstack.instances.api import Instances as OpenStackInstance
from fleio.openstack.settings import plugin_settings
from fleio.openstack.api.session import get_session
from django.conf import settings
LOG = logging.getLogger(__name__)


def send_ticket(
        vpn_user: str,
        vpn_password: str,
        ip_user: str,
        admin_user: AppUser,
        client: Client
        ) -> Response:
    description = settings.VPN_MESSAGE_TEMPLATE.format(
        ip_user=ip_user,
        vpn_user=vpn_user,
        vpn_password=vpn_password)

    ticket_data = {
        'title': settings.VPN_MESSAGE_TITLE,
        'description': description,
        'department': settings.VPN_TICKET_DEPARTMENT,
        'priority': 'medium',
    }

    serializer = TicketCreateSerializer(data=ticket_data, context={'request': None})
    if serializer.is_valid(raise_exception=True):
        ticket = serializer.save(created_by=admin_user, client=client)
        return Response({
            'message': f'Found instance with IP {ip_user} and created ticket {ticket.id}.'
        }, status=201)
    return Response({'message': 'Failed to create ticket.'}, status=400)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def public_vpn_notification(request):
    #ip_user = request.META.get('HTTP_X_FORWARDED_FOR')
    ip_user = request.data.get('ip_address')
    vpn_user = request.data.get('vpn_user')
    vpn_password = request.data.get('vpn_password')
    admin_user = AppUser.objects.get(id=settings.VPN_ADMIN_APPUSER)
    now = datetime.now(timezone.utc)
    five_minutes_ago = now - timedelta(minutes=5)

    if not vpn_user or not vpn_password or not ip_user:
        return Response({'message': 'Not all data was provided'}, status=400)

    if ip_user:
        # HTTP_X_FORWARDED_FOR can contain several IP addresses, take the first one
        ip_user = ip_user.split(',')[0].strip()

    ip_tracker = InstanceIPTracker.objects.filter(ip_address=ip_user)
    if not ip_tracker.exists():
        return Response({'message': 'No Instance found for the provided IP address.'}, status=404)

    port = ip_tracker.first().port
    if not port:
        return Response({'message': 'No port found for the provided IP address.'}, status=404)

    items = Instance.objects.filter(ports__id=port.id)

    if not items.exists():
        return Response({'message': 'No Instance found for the provided IP address.'}, status=404)
    item = items.first()
    client = item.project.service.client

    scoped_session = get_session(
        auth_url=plugin_settings.AUTH_URL,
        project_id=item.project_id,
        project_domain_id=plugin_settings.PROJECT_DOMAIN_ID,
        admin_username=plugin_settings.USERNAME,
        admin_password=plugin_settings.PASSWORD,
        admin_domain_id=plugin_settings.USER_DOMAIN_ID,
        api_version='3',
        verify=plugin_settings.require_valid_ssl,
        timeout=plugin_settings.TIMEOUT,
    )

    actions, has_more = OpenStackInstance(api_session=scoped_session).get(item).get_actions()

    action_found = any(
        action['action'] in ['rebuild', 'create'] and action['start_time'] >= five_minutes_ago
        for action in actions
    )

    if not action_found:
        return Response({'message': 'No rebuild or activate actions found in the last 5 minutes.'}, status=404)

    return send_ticket(vpn_user, vpn_password, ip_user, admin_user, client)
