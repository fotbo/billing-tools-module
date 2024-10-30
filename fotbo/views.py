from rest_framework import permissions
import logging
from django.db.models import Q
from fleio.openstack.models import Instance
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from plugins.tickets.enduser.tickets.serializers import TicketCreateSerializer
from fleio.core.models import AppUser
from datetime import datetime, timedelta, timezone
LOG = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def public_view(request):
    # ip_user = request.META.get('HTTP_X_FORWARDED_FOR')
    ip_user = request.data.get('ip_address')
    ovpn_user = request.data.get('ovpn_user')
    ovpn_password = request.data.get('ovpn_password')
    admin_user = AppUser.objects.get(id=752917) 
    now = datetime.now(timezone.utc)
    five_minutes_ago = now - timedelta(minutes=5)

    if not ovpn_user or not ovpn_password or not ip_user:
        return Response({'message': 'Not all data was provided'}, status=400)

    if ip_user:
        # HTTP_X_FORWARDED_FOR can contain several IP addresses, take the first one
        ip_user = ip_user.split(',')[0].strip()

    items = Instance.objects.filter(
        Q(addresses__icontains=f'"address": "{ip_user}"')
    )

    if not items.exists():
        return Response({'message': 'No Instance found for the provided IP address.'}, status=404)
    item = items.first()

    if not item.project.service.client.users.exists():
        return Response({'message': 'No user found for the provided IP address.'}, status=404)
    user = item.project.service.client.users.first()

    recent_action = any(
        action.action in ['rebuild', 'create'] and action.start_time >= five_minutes_ago
        for action in item.actions.all()
    )
    if not recent_action:
        return Response({'message': 'There was no rebuild or create in 5 minutes'}, status=400)

    data = {
        'title': f'Login and Password for OVPN Server {ip_user}',
        'description': (
            f"<b>OVPN Server Details</b><br>"
            f"----------------------<br>"
            f"URL: https://{ip_user}<br>"
            f"User: {ovpn_user}<br>"
            f"Password: {ovpn_password}<br>"
        ),
        'department': 1,
        'priority': 'medium',
    }

    serializer = TicketCreateSerializer(data=data, context={'request': None})
    if serializer.is_valid(raise_exception=True):
        ticket = serializer.save(created_by=admin_user, assigned_to=user)
        return Response({'message': f'Found {items.count()} Instance with IP {ip_user} '
                                    f'and created ticket {ticket.id}.'}, status=200)
    else:
        return Response({'message': 'Failed to create ticket.'}, status=400)



