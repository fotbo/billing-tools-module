from dataclasses import dataclass
from django.conf import settings
from rest_framework import serializers
from ipaddress import (
    ip_address, ip_network,
    IPv4Address, IPv4Network, IPv6Address, IPv6Network
    )
import logging

LOG = logging.getLogger(__name__)


@dataclass
class ApiValidator:

    def check_if_required(
            self,
            source_ip,
            destination_ip,
            direction,
            instance_id) -> None | Exception:
        if direction == 'in' and source_ip is None:
            raise serializers.ValidationError('Source IP is required')
        if direction == 'out' and destination_ip is None:
            raise serializers.ValidationError('Destination IP is required')
        if instance_id is None:
            raise serializers.ValidationError('Instance id is required')

    def check_v4(self, ip: str, net: str) -> None | Exception:
        if IPv4Address(ip) not in IPv4Network(net) and net in settings.EXLUDED_PRIVATE_NETWORK:
            if ip_address(ip).is_private:
                LOG.info(f'{ip} is private')
                raise serializers.ValidationError(
                                'IP can not be private. Allow only global IPs')

        if IPv4Address(ip) in IPv4Network(net) and net in settings.RESERVED_NETWORK:
            LOG.info(f'Attempting to block a IP address from RESERVED_NETWORK - {ip}')
            raise serializers.ValidationError(
                                'This IP address is not allowed to be added to the firewall.')

    def check_v6(self, ip: str, net: str) -> None | Exception:
        if IPv6Address(ip) not in IPv6Network(net) and net in settings.EXLUDED_PRIVATE_NETWORK:
            if ip_address(ip).is_private:
                LOG.info(f'{ip} is private')
                raise serializers.ValidationError(
                                'IP can not be private. Allow only global IPs'
                                )
        if IPv6Address(ip) in IPv6Network(net) and net in settings.RESERVED_NETWORK:
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
        if ip in settings.SYSTEM_IPS:
            LOG.info('Attempting to block a system IP address')
            raise serializers.ValidationError(
                                'This IP address is not allowed to be added to the firewall.')
        if ip_address(ip).version == 4:
            last_octet = int(ip.split('.')[-1])
            if last_octet < 3:
                LOG.info('Attempting to block a gateway')
                raise serializers.ValidationError(
                                'This IP address is not allowed to be added to the firewall.'
                                )


    def validate_add_filter_rule(self, action, direction, ipprotocol, protocol) -> bool:
        if action not in ["pass", "block", "reject"]:
            raise ValueError(f"Invalid `action`: {action}, must be `pass`, `block`, or `reject`")

        if direction not in ["in", "out"]:
            raise ValueError(f"Invalid `direction`: {direction}, must be `in` or `out`")

        if ipprotocol not in ["inet", "inet6"]:
            raise ValueError(f"Invalid `ipprotocol`: {ipprotocol}, must be `inet` or `inet6`")

        if protocol not in ["any", "ICMP", "IGMP", "GGP", "IPENCAP", "ST2", "TCP", "CBT", "EGP", "IGP", "BBN-RCC", "NVP",
                            "PUP", "ARGUS", "EMCON", "XNET", "CHAOS", "UDP", "MUX", "DCN", "HMP", "PRM", "XNS-IDP",
                            "TRUNK-1", "TRUNK-2", "LEAF-1", "LEAF-2", "RDP", "IRTP", "ISO-TP4", "NETBLT", "MFE-NSP",
                            "MERIT-INP", "DCCP", "3PC", "IDPR", "XTP", "DDP", "IDPR-CMTP", "TP++", "IL", "IPV6", "SDRP",
                            "IDRP", "RSVP", "GRE", "DSR", "BNA", "ESP", "AH", "I-NLSP", "SWIPE", "NARP", "MOBILE", "TLSP",
                            "SKIP", "IPV6-ICMP", "CFTP", "SAT-EXPAK", "KRYPTOLAN", "RVD", "IPPC", "SAT-MON", "VISA", "IPCV",
                            "CPNX", "CPHB", "WSN", "PVP", "BR-SAT-MON", "SUN-ND", "WB-MON", "WB-EXPAK", "ISO-IP", "VMTP",
                            "SECURE-VMTP", "VINES", "TTP", "NSFNET-IGP", "DGP", "TCF", "EIGRP", "OSPF", "SPRITE-RPC",
                            "LARP", "MTP", "AX.25", "IPIP", "MICP", "SCC-SP", "ETHERIP", "ENCAP", "GMTP", "IFMP", "PNNI",
                            "PIM", "ARIS", "SCPS", "QNX", "A/N", "IPCOMP", "SNP", "COMPAQ-PEER", "IPX-IN-IP", "CARP", "PGM",
                            "L2TP", "DDX", "IATP", "STP", "SRP", "UTI", "SMP", "SM", "PTP", "ISIS", "CRTP", "CRUDP", "SPS",
                            "PIPE", "SCTP", "FC", "RSVP-E2E-IGNORE", "UDPLITE", "MPLS-IN-IP", "MANET", "HIP", "SHIM6",
                            "WESP", "ROHC", "PFSYNC", "DIVERT"]:
            raise ValueError(
                f"Invalid `protocol`: {protocol}, must be `any`, `ICMP`, `IGMP`, `GGP`, `IPENCAP`, `ST2`, `TCP`, `CBT`, "
                f"`EGP`, `IGP`, `BBN-RCC`, `NVP`, `PUP`, `ARGUS`, `EMCON`, `XNET`, `CHAOS`, `UDP`, `MUX`, `DCN`, `HMP`, "
                f"`PRM`, `XNS-IDP`, `TRUNK-1`, `TRUNK-2`, `LEAF-1`, `LEAF-2`, `RDP`, `IRTP`, `ISO-TP4`, `NETBLT`, "
                f"`MFE-NSP`, `MERIT-INP`, `DCCP`, `3PC`, `IDPR`, `XTP`, `DDP`, `IDPR-CMTP`, `TP++`, `IL`, `IPV6`, `SDRP`, "
                f"`IDRP`, `RSVP`, `GRE`, `DSR`, `BNA`, `ESP`, `AH`, `I-NLSP`, `SWIPE`, `NARP`, `MOBILE`, `TLSP`, `SKIP`, "
                f"`IPV6-ICMP`, `CFTP`, `SAT-EXPAK`, `KRYPTOLAN`, `RVD`, `IPPC`, `SAT-MON`, `VISA`, `IPCV`, `CPNX`, "
                f"`CPHB`, `WSN`, `PVP`, `BR-SAT-MON`, `SUN-ND`, `WB-MON`, `WB-EXPAK`, `ISO-IP`, `VMTP`, `SECURE-VMTP`, "
                f"`VINES`, `TTP`, `NSFNET-IGP`, `DGP`, `TCF`, `EIGRP`, `OSPF`, `SPRITE-RPC`, `LARP`, `MTP`, `AX.25`, "
                f"`IPIP`, `MICP`, `SCC-SP`, `ETHERIP`, `ENCAP`, `GMTP`, `IFMP`, `PNNI`, `PIM`, `ARIS`, `SCPS`, `QNX`, "
                f"`A/N`, `IPCOMP`, `SNP`, `COMPAQ-PEER`, `IPX-IN-IP`, `CARP`, `PGM`, `L2TP`, `DDX`, `IATP`, `STP`, `SRP`, "
                f"`UTI`, `SMP`, `SM`, `PTP`, `ISIS`, `CRTP`, `CRUDP`, `SPS`, `PIPE`, `SCTP`, `FC`, `RSVP-E2E-IGNORE`, "
                f"`UDPLITE`, `MPLS-IN-IP`, `MANET`, `HIP`, `SHIM6`, `WESP`, `ROHC`, `PFSYNC`, or `DIVERT`")

        return True

validator = ApiValidator()