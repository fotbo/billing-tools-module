from django.db import models
from fleio.core.models import Client
from cryptography.fernet import Fernet
from django.conf import settings


class FwDeviceType(models.TextChoices):
    ARISTA = 'Arista'
    OPNSENCE = 'OPNsense'


class FwAction(models.TextChoices):
    ALLOW = 'pass'
    BLOCK = 'block'


class FwDirection(models.TextChoices):
    INPUT = 'in'
    OUTPUT = 'out'


class FwProtocol(models.TextChoices):
    ANY = 'any'
    ICMP = 'ICMP'
    IGMP = 'IGMP'
    GGP = 'GGP'
    IPENCAP = 'IPENCAP'
    ST2 = 'ST2'
    TCP = 'TCP'
    CBT = 'CBT'
    EGP = 'EGP'
    IGP = 'IGP'
    BBN_RCC = 'BBN-RCC'
    NVP = 'NVP'
    PUP = 'PUP'
    ARGUS = 'ARGUS'
    EMCON = 'EMCON'
    XNET = 'XNET'
    CHAOS = 'CHAOS'
    UDP = 'UDP'
    MUX = 'MUX'
    DCN = 'DCN'
    HMP = 'HMP'
    PRM = 'PRM'
    XNS_IDP = 'XNS-IDP'
    TRUNK_1 = 'TRUNK-1'
    TRUNK_2 = 'TRUNK-2'
    LEAF_1 = 'LEAF-1'
    LEAF_2 = 'LEAF-2'
    RDP = 'RDP'
    IRTP = 'IRTP'
    ISO_TP4 = 'ISO-TP4'
    NETBLT = 'NETBLT'
    MFE_NSP = 'MFE-NSP'
    MERIT_INP = 'MERIT-INP'
    DCCP = 'DCCP'
    _3PC = '3PC'
    IDPR = 'IDPR'
    XTP = 'XTP'
    DDP = 'DDP'
    IDPR_CMTP = 'IDPR-CMTP'
    TP_PP = 'TP++'
    IL = 'IL'
    IPV6 = 'IPV6'
    SDRP = 'SDRP'
    IDRP = 'IDRP'
    RSVP = 'RSVP'
    GRE = 'GRE'
    DSR = 'DSR'
    BNA = 'BNA'
    ESP = 'ESP'
    AH = 'AH'
    I_NLSP = 'I-NLSP'
    SWIPE = 'SWIPE'
    NARP = 'NARP'
    MOBILE = 'MOBILE'
    TLSP = 'TLSP'
    SKIP = 'SKIP'
    IPV6_ICMP = 'IPV6-ICMP'
    CFTP = 'CFTP'
    SAT_EXPAK = 'SAT-EXPAK'
    KRYPTOLAN = 'KRYPTOLAN'
    RVD = 'RVD'
    IPPC = 'IPPC'
    SAT_MON = 'SAT-MON'
    VISA = 'VISA'
    IPCV = 'IPCV'
    CPNX = 'CPNX'
    CPHB = 'CPHB'
    WSN = 'WSN'
    PVP = 'PVP'
    BR_SAT_MON = 'BR-SAT-MON'
    SUN_ND = 'SUN-ND'
    WB_MON = 'WB-MON'
    WB_EXPAK = 'WB-EXPAK'
    ISO_IP = 'ISO-IP'
    VMTP = 'VMTP'
    SECURE_VMTP = 'SECURE-VMTP'
    VINES = 'VINES'
    TTP = 'TTP'
    NSFNET_IGP = 'NSFNET-IGP'
    DGP = 'DGP'
    TCF = 'TCF'
    EIGRP = 'EIGRP'
    OSPF = 'OSPF'
    SPRITE_RPC = 'SPRITE-RPC'
    LARP = 'LARP'
    MTP = 'MTP'
    AX_25 = 'AX.25'
    IPIP = 'IPIP'
    MICP = 'MICP'
    SCC_SP = 'SCC-SP'
    ETHERIP = 'ETHERIP'
    ENCAP = 'ENCAP'
    GMTP = 'GMTP'
    IFMP = 'IFMP'
    PNNI = 'PNNI'
    PIM = 'PIM'
    ARIS = 'ARIS'
    SCPS = 'SCPS'
    QNX = 'QNX'
    A_N = 'A/N'
    IPCOMP = 'IPCOMP'
    SNP = 'SNP'
    COMPAQ_PEER = 'COMPAQ-PEER'
    IPX_IN_IP = 'IPX-IN-IP'
    CARP = 'CARP'
    PGM = 'PGM'
    L2TP = 'L2TP'
    DDX = 'DDX'
    IATP = 'IATP'
    STP = 'STP'
    SRP = 'SRP'
    UTI = 'UTI'
    SMP = 'SMP'
    SM = 'SM'
    PTP = 'PTP'
    ISIS = 'ISIS'
    CRTP = 'CRTP'
    CRUDP = 'CRUDP'
    SPS = 'SPS'
    PIPE = 'PIPE'
    SCTP = 'SCTP'
    FC = 'FC'
    RSVP_E2E_IGNORE = 'RSVP-E2E-IGNORE'
    UDPLITE = 'UDPLITE'
    MPLS_IN_IP = 'MPLS-IN-IP'
    MANET = 'MANET'
    HIP = 'HIP'
    SHIM6 = 'SHIM6'
    WESP = 'WESP'
    ROHC = 'ROHC'
    PFSYNC = 'PFSYNC'
    DIVERT = 'DIVERT'


class FwInterface(models.TextChoices):
    PUBLIC_NET_V4_V6 = 'opt1'


class FwRegions(models.Model):
    name = models.CharField(max_length=255)
    api_key_encrypted = models.CharField(max_length=255)
    api_secret_encrypted = models.CharField(max_length=255)
    api_url = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50, choices=FwDeviceType.choices)

    @property
    def api_key(self):
        cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        return cipher_suite.decrypt(self.api_key_encrypted).decode()

    @api_key.setter
    def api_key(self, api_key):
        cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        self.api_key_encrypted = cipher_suite.encrypt(api_key.encode()).decode("utf-8")

    @property
    def api_secret(self):
        cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        return cipher_suite.decrypt(self.api_secret_encrypted).decode()

    @api_secret.setter
    def api_secret(self, api_secret):
        cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        self.api_secret_encrypted = cipher_suite.encrypt(api_secret.encode()).decode("utf-8")


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
    firewall_uuid = models.CharField(max_length=128, null=True)
    instance_id = models.CharField(max_length=256, null=True)
    action = models.CharField(max_length=50, choices=FwAction.choices, default=FwAction.BLOCK)
    direction = models.CharField(max_length=50, choices=FwDirection.choices, default=FwDirection.INPUT)
    interface = models.JSONField(max_length=255, null=True)
    protocol = models.CharField(max_length=50, choices=FwProtocol.choices, default=FwProtocol.ANY)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client} - {self.region}"
