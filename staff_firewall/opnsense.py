from dataclasses import dataclass
from typing import Dict
from .models import FwStaff
from .opnsense_api import Opnsense


@dataclass
class RuleManager:

    def opnsense_request(self, conf: object):
        opnsense = Opnsense(
                api_url=conf.api_url,
                api_key=conf.api_key,
                api_secret=conf.api_secret)
        return opnsense.firewall.filter_controller

    def add(self, conf: object, validated_data: dict) -> str:
        firewall = self.opnsense_request(conf)
        return firewall.add_rule(
                direction=validated_data.get('direction', None),
                interface=validated_data.get('interface', None),
                source_net=validated_data.get('source_ip', None),
                destination_net=validated_data.get('destination_ip', None),
                action=validated_data.get('action'),
                protocol=validated_data.get('protocol'),
                source_port=validated_data.get('source_port', 0),
                destination_port=validated_data.get('destination_port', 0),
                description=validated_data.get('description', 0),
                enabled=validated_data.get('enabled'),
                ipprotocol=validated_data.get('ip_version')
                )

    def update(self, conf: object, instance: object, validated_data: dict) -> Dict[any, any]:
        firewall = self.opnsense_request(conf)
        firewall_uuid = FwStaff.objects.filter(
            id=instance.pk
            ).first().firewall_uuid
        return firewall.set_rule(
                uuid=firewall_uuid,
                direction=validated_data.get('direction', None),
                interface=validated_data.get('interface', None),
                source_net=validated_data.get('source_ip', None),
                destination_net=validated_data.get('destination_ip', None),
                action=validated_data.get('action'),
                protocol=validated_data.get('protocol'),
                source_port=validated_data.get('source_port', 0),
                destination_port=validated_data.get('destination_port', 0),
                description=f"Client - {validated_data.get('client')} | {validated_data.get('description', 0)}",
                enabled=validated_data.get('enabled'),
                )

    def delete(self, conf: object, instance: object) -> None:
        firewall = self.opnsense_request(conf)
        firewall_uuid = FwStaff.objects.filter(
            id=instance.pk).first().firewall_uuid
        if firewall.get_rule(firewall_uuid) is not None:
            firewall.delete_rule(uuid=firewall_uuid)

    def toogle(self, conf: object, firewall_uuid: str) -> dict:
        firewall = self.opnsense_request(conf)
        return firewall.toggle_rule(firewall_uuid)


rule_manager = RuleManager()
