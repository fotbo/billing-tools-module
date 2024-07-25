from fleio.celery import app
from fleio.openstack.models import Instance

from .models import FwStaff

@app.task(name='Cleanup firewall rule', do_not_create_activity=True)
def cleanup_firewall_rule():
    rules  = FwStaff.objects.all()
    for rule in rules:
        print(rule.destination_ip)