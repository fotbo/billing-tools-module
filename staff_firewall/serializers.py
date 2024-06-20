from typing import Dict
from ipaddress import ip_address, ip_network ,IPv4Address, IPv4Network, IPv6Address, IPv6Network
import logging

from django.conf import settings
from rest_framework import serializers

from .models import FwStaff, Client, FwRegions
from .opnsence import rule_manager


LOG = logging.getLogger(__name__)


class FwStaffSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(
        queryset=FwRegions.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = FwStaff
        fields = '__all__'

    def check_v4(self, ip: str, net: str) -> None | Exception:
        if IPv4Address(ip) not in IPv4Network(net):
            if ip_address(ip).is_private:
                LOG.info(f'{ip} is private')
                raise serializers.ValidationError(
                                'IP can not be private. Allow only global IPs')

        if IPv4Address(ip) in IPv4Network(net):
            LOG.info(f'Attempting to block a reserved or system IP address - {ip}')
            raise serializers.ValidationError(
                                'This IP address is not allowed to be added to the firewall.')

    def check_v6(self, ip: str, net: str) -> None | Exception:
        if IPv6Address(ip) not in IPv6Network(net):
            if ip_address(ip).is_private:
                LOG.info(f'{ip} is private')
                raise serializers.ValidationError(
                                'IP can not be private. Allow only global IPs'
                                )
        if IPv6Address(ip) in IPv6Network(net):
            LOG.info(f'Attempting to block a reserved or system IP address - {ip}')
            raise serializers.ValidationError(
                                'This IP address is not allowed to be added to the firewall.'
                                )

    def is_private(self, ip: str) -> None | Exception:
        try:
            settings.EXLUDED_PRIVATE_NETWORK
        except Exception:
            LOG.info('Variable EXLUDED_PRIVATE_NETWORK is not defined')
            pass
        if settings.EXLUDED_PRIVATE_NETWORK:
            for net in settings.EXLUDED_PRIVATE_NETWORK:
                if ip_network(net).version == 4 and ip_address(ip).version == 4:
                    self.check_v4(ip, net)
                elif ip_network(net).version == 6 and ip_address(ip).version == 6:
                    self.check_v6(ip, net)
        else:
            LOG.info('Var EXLUDED_PRIVATE_NETWORK is empty')
            raise serializers.ValidationError(
                'EXLUDED_PRIVATE_NETWORK can not be empty'
                )

    def is_reserved_network(self, ip: str) -> None | Exception:
        try:
            settings.RESERVED_NETWORK
        except Exception:
            LOG.info('Variable RESERVED_NETWORK is not defined')
            pass
        if settings.RESERVED_NETWORK:
            for net in settings.RESERVED_NETWORK:
                if ip_network(net).version == 4 and ip_address(ip).version == 4:
                    self.check_v4(ip, net)
                elif ip_network(net).version == 6 and ip_address(ip).version == 6:
                    self.check_v6(ip, net)
        else:
            LOG.info('Var RESERVED_NETWORK is empty')
            raise serializers.ValidationError(
                'RESERVED_NETWORK can not be empty'
                )

    def is_reserved_ip(self, ip):
        if ip_address(ip).version == 4:
            last_octet = int(ip.split('.')[-1])
            if last_octet < 13:
                LOG.info('Attempting to block a reserved or system IP address')
                raise serializers.ValidationError(
                                'This IP address is not allowed to be added to the firewall.'
                                )

    def ip_validator(self, ip: str) -> None:
        self.is_private(ip)
        self.is_reserved_network(ip)
        self.is_reserved_ip(ip)

    def validate(self, attrs):
        destination_ip = attrs.get('destination_ip')
        source_ip = attrs.get('source_ip')
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
