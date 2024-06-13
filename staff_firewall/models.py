from django.db import models
from fleio.core.models import Client


class FwDeviceType(models.TextChoices):
    ARISTA = 'Arista'
    OPNSENCE = 'OPNsence'

class FwAction(models.TextChoices):
    ALLOW = 'pass'
    BLOCK = 'block'

class FwDirection(models.TextChoices):
    INPUT  = 'in'
    OUTPUT = 'out'

class FwProtocol(models.TextChoices):
    ANY = 'any'
    TCP = 'tcp'
    UDP = 'udp'

class FwInterface(models.TextChoices):
    PUBLIC_NET_V4_V6 = 'opt1'
    PUBLIC_NET_V6_ONLY = None

class FwRegions(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    api_url = models.URLField()
    device_type = models.CharField(max_length=50, choices=FwDeviceType.choices)

    def __str__(self):
        return self.name


class FwStaff(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    region = models.ForeignKey(FwRegions, on_delete=models.CASCADE)
    destination_ip = models.GenericIPAddressField(null=True)
    destination_port = models.IntegerField(null=True)
    source_ip = models.GenericIPAddressField(null=True)
    source_port = models.IntegerField(null=True)
    description = models.CharField(max_length=255, null=True)
    firewall_uuid = models.UUIDField(max_length=128, null=True)
    action = models.CharField(max_length=50, choices=FwAction.choices, default=FwAction.BLOCK)
    direction = models.CharField(max_length=50, choices=FwDirection.choices, default=FwDirection.INPUT)
    interface = models.CharField(max_length=50, choices=FwInterface.choices, null=True)
    protocol  = models.CharField(max_length=50, choices=FwProtocol.choices, default=FwProtocol.ANY)

    def __str__(self):
        return f"{self.client} - {self.region}"

