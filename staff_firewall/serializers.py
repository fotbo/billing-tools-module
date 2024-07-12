from typing import Dict
import logging
from rest_framework import serializers

from .models import FwStaff, Client, FwRegions
from .opnsence import rule_manager
from .opnsense_api.util.validate import validator

LOG = logging.getLogger(__name__)


class FwStaffSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(
        queryset=FwRegions.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = FwStaff
        fields = '__all__'

    def ip_validator(self, ip: str) -> None:
        validator.is_private(ip)
        validator.is_reserved_network(ip)
        validator.is_reserved_ip(ip)

    def validate(self, attrs):
        destination_ip = attrs.get('destination_ip', None)
        source_ip = attrs.get('source_ip', None)
        validator.check_if_required(
                destination_ip=destination_ip,
                source_ip=source_ip,
                direction=attrs.get('direction'),
                instance_id=attrs.get('instance_id', None)
                )
        if destination_ip:
            self.ip_validator(destination_ip)
        if source_ip:
            self.ip_validator(source_ip)
        return super().validate(attrs)

    def conf_by_region(self, region: str) -> object:
        return FwRegions.objects.filter(name=region).first()

    def create(self, validated_data: dict) -> Dict[any, any]:
        conf_by_region = self.conf_by_region(validated_data.get('region'))
        if str(conf_by_region.device_type) == 'OPNsense':
            validated_data['description'] = f" {validated_data.get('description', 0)} | {validated_data.get('client')}"
            validated_data['firewall_uuid'] = rule_manager.add(
                conf=conf_by_region,
                validated_data=validated_data).get('uuid')
        return super().create(validated_data)

    def update(self, instance, validated_data: dict) -> Dict[any, any]:
        conf_by_region = self.conf_by_region(validated_data.get('region'))
        if str(conf_by_region.device_type) == 'OPNsense':
            rule_manager.update(
                conf=conf_by_region,
                instance=instance,
                validated_data=validated_data)
        return super().update(instance, validated_data)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']


class FwRegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FwRegions
        fields = ['name']


class FwStaffDetailSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    region = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = FwStaff
        fields = '__all__'
