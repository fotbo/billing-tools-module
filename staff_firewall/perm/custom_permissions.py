import logging
from typing import List

from django.utils.translation import gettext_lazy as _

from fleio.core.models.permission_definitions import PermissionNames
from fleio.core.models.permission import Permission
from fleio.core.models.permission_set import PermissionSet

LOG = logging.getLogger(__name__)


class CustomPermissionNames(PermissionNames):

    staff_firewall_list = 'staff_firewall.list'
    staff_firewall_create = 'staff_firewall.create'
    staff_firewall_destroy = 'staff_firewall.None'

    custom_web_edition_only_permissions = [
        staff_firewall_list, staff_firewall_create, staff_firewall_destroy]

    custom_openstack_edition_only_permissions = [
        staff_firewall_list, staff_firewall_create, staff_firewall_destroy]


    custom_staff_permissions = [
        staff_firewall_list, staff_firewall_create, staff_firewall_destroy]

    custom_permissions_map = {
        staff_firewall_list: _('Staff firewall- List '),
        staff_firewall_create: _('Staff firewall - Create'),
        staff_firewall_destroy: _('Staff firewall - delete')
    }

    def init_perm(self) -> None:
        self.permissions_map.update(self.custom_permissions_map)
        self.web_edition_only_permissions.extend(self.custom_web_edition_only_permissions)
        self.openstack_edition_only_permissions.extend(self.custom_openstack_edition_only_permissions)
        self.custom_staff_permissions.extend(self.custom_staff_permissions)


perm = CustomPermissionNames()