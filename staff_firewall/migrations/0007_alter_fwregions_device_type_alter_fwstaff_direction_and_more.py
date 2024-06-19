# Generated by Django 4.2.5 on 2024-06-18 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff_firewall", "0006_remove_fwstaff_dst_port_remove_fwstaff_ip_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fwregions",
            name="device_type",
            field=models.CharField(
                choices=[("Arista", "Arista"), ("OPNsense", "Opnsence")], max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="fwstaff",
            name="direction",
            field=models.CharField(
                choices=[("in", "Input"), ("out", "Output")],
                default="in",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="fwstaff",
            name="interface",
            field=models.JSONField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="fwstaff",
            name="protocol",
            field=models.CharField(
                choices=[
                    ("any", "Any"),
                    ("ICMP", "Icmp"),
                    ("IGMP", "Igmp"),
                    ("GGP", "Ggp"),
                    ("IPENCAP", "Ipencap"),
                    ("ST2", "St2"),
                    ("TCP", "Tcp"),
                    ("CBT", "Cbt"),
                    ("EGP", "Egp"),
                    ("IGP", "Igp"),
                    ("BBN-RCC", "Bbn Rcc"),
                    ("NVP", "Nvp"),
                    ("PUP", "Pup"),
                    ("ARGUS", "Argus"),
                    ("EMCON", "Emcon"),
                    ("XNET", "Xnet"),
                    ("CHAOS", "Chaos"),
                    ("UDP", "Udp"),
                    ("MUX", "Mux"),
                    ("DCN", "Dcn"),
                    ("HMP", "Hmp"),
                    ("PRM", "Prm"),
                    ("XNS-IDP", "Xns Idp"),
                    ("TRUNK-1", "Trunk 1"),
                    ("TRUNK-2", "Trunk 2"),
                    ("LEAF-1", "Leaf 1"),
                    ("LEAF-2", "Leaf 2"),
                    ("RDP", "Rdp"),
                    ("IRTP", "Irtp"),
                    ("ISO-TP4", "Iso Tp4"),
                    ("NETBLT", "Netblt"),
                    ("MFE-NSP", "Mfe Nsp"),
                    ("MERIT-INP", "Merit Inp"),
                    ("DCCP", "Dccp"),
                    ("3PC", " 3Pc"),
                    ("IDPR", "Idpr"),
                    ("XTP", "Xtp"),
                    ("DDP", "Ddp"),
                    ("IDPR-CMTP", "Idpr Cmtp"),
                    ("TP++", "Tp Pp"),
                    ("IL", "Il"),
                    ("IPV6", "Ipv6"),
                    ("SDRP", "Sdrp"),
                    ("IDRP", "Idrp"),
                    ("RSVP", "Rsvp"),
                    ("GRE", "Gre"),
                    ("DSR", "Dsr"),
                    ("BNA", "Bna"),
                    ("ESP", "Esp"),
                    ("AH", "Ah"),
                    ("I-NLSP", "I Nlsp"),
                    ("SWIPE", "Swipe"),
                    ("NARP", "Narp"),
                    ("MOBILE", "Mobile"),
                    ("TLSP", "Tlsp"),
                    ("SKIP", "Skip"),
                    ("IPV6-ICMP", "Ipv6 Icmp"),
                    ("CFTP", "Cftp"),
                    ("SAT-EXPAK", "Sat Expak"),
                    ("KRYPTOLAN", "Kryptolan"),
                    ("RVD", "Rvd"),
                    ("IPPC", "Ippc"),
                    ("SAT-MON", "Sat Mon"),
                    ("VISA", "Visa"),
                    ("IPCV", "Ipcv"),
                    ("CPNX", "Cpnx"),
                    ("CPHB", "Cphb"),
                    ("WSN", "Wsn"),
                    ("PVP", "Pvp"),
                    ("BR-SAT-MON", "Br Sat Mon"),
                    ("SUN-ND", "Sun Nd"),
                    ("WB-MON", "Wb Mon"),
                    ("WB-EXPAK", "Wb Expak"),
                    ("ISO-IP", "Iso Ip"),
                    ("VMTP", "Vmtp"),
                    ("SECURE-VMTP", "Secure Vmtp"),
                    ("VINES", "Vines"),
                    ("TTP", "Ttp"),
                    ("NSFNET-IGP", "Nsfnet Igp"),
                    ("DGP", "Dgp"),
                    ("TCF", "Tcf"),
                    ("EIGRP", "Eigrp"),
                    ("OSPF", "Ospf"),
                    ("SPRITE-RPC", "Sprite Rpc"),
                    ("LARP", "Larp"),
                    ("MTP", "Mtp"),
                    ("AX.25", "Ax 25"),
                    ("IPIP", "Ipip"),
                    ("MICP", "Micp"),
                    ("SCC-SP", "Scc Sp"),
                    ("ETHERIP", "Etherip"),
                    ("ENCAP", "Encap"),
                    ("GMTP", "Gmtp"),
                    ("IFMP", "Ifmp"),
                    ("PNNI", "Pnni"),
                    ("PIM", "Pim"),
                    ("ARIS", "Aris"),
                    ("SCPS", "Scps"),
                    ("QNX", "Qnx"),
                    ("A/N", "A N"),
                    ("IPCOMP", "Ipcomp"),
                    ("SNP", "Snp"),
                    ("COMPAQ-PEER", "Compaq Peer"),
                    ("IPX-IN-IP", "Ipx In Ip"),
                    ("CARP", "Carp"),
                    ("PGM", "Pgm"),
                    ("L2TP", "L2Tp"),
                    ("DDX", "Ddx"),
                    ("IATP", "Iatp"),
                    ("STP", "Stp"),
                    ("SRP", "Srp"),
                    ("UTI", "Uti"),
                    ("SMP", "Smp"),
                    ("SM", "Sm"),
                    ("PTP", "Ptp"),
                    ("ISIS", "Isis"),
                    ("CRTP", "Crtp"),
                    ("CRUDP", "Crudp"),
                    ("SPS", "Sps"),
                    ("PIPE", "Pipe"),
                    ("SCTP", "Sctp"),
                    ("FC", "Fc"),
                    ("RSVP-E2E-IGNORE", "Rsvp E2E Ignore"),
                    ("UDPLITE", "Udplite"),
                    ("MPLS-IN-IP", "Mpls In Ip"),
                    ("MANET", "Manet"),
                    ("HIP", "Hip"),
                    ("SHIM6", "Shim6"),
                    ("WESP", "Wesp"),
                    ("ROHC", "Rohc"),
                    ("PFSYNC", "Pfsync"),
                    ("DIVERT", "Divert"),
                ],
                default="any",
                max_length=50,
            ),
        ),
    ]