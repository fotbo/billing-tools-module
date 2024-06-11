from django.db import models
from fleio.core.models import Client


class FwDeviceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FwRegions(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    api_url = models.URLField()
    device_type = models.ForeignKey(FwDeviceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FwActions(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FwStaff(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    region = models.ForeignKey(FwRegions, on_delete=models.CASCADE)
    ip = models.CharField(max_length=255)
    dst_port = models.IntegerField(default=0)
    src_port = models.IntegerField(default=0)
    action = models.ForeignKey(FwActions, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client} - {self.regions} - {self.ip}"

