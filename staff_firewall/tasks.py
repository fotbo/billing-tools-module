import logging
from fleio.celery import app
from fleio.openstack.models import Instance

from .models import FwStaff, FwRegions
 from .opnsense import rule_manager

LOG = logging.getLogger(__name__)


@app.task(name='Cleanup firewall rule', do_not_create_activity=True)
def cleanup_firewall_rule() -> None:
    rules = FwStaff.objects.all()
    for rule in rules:
        try:
            Instance.objects.get(id=rule.instance_id)
            LOG.info(f'The rule with instance id {rule.instance_id} is still exists.')
        except Instance.DoesNotExist:
            if rule.region.device_type == 'OPNsense':
                conf_by_region = FwRegions.objects.filter(
                    name=rule.region
                    ).first()
                rule_manager.delete(conf=conf_by_region, instance=rule)
                rule.delete()
                LOG.info(
                    f'The rule with instance id {rule.instance_id} was deleted.'
                    )