"""Contains Python objects for IP and network layer datagrams/segments."""

from __future__ import unicode_literals
from struct import unpack
from abc import ABCMeta
from abc import abstractmethod
import socket

# A list of IP Protocol numbers, taken directly from IANA.
PROTO_NUMS = {
    0: 'HOPOPT',
    1: 'ICMP',
    2: 'IGMP',
    3: 'GGP',
    4: 'IPv4',
    5: 'ST',
    6: 'TCP',
    7: 'CBT',
    8: 'EGP',
    9: 'IGP',
    10: 'BBN-RCC-MON',
    11: 'NVP-II',
    12: 'PUP',
    13: 'ARGUS',
    14: 'EMCON',
    15: 'XNET',
    16: 'CHAOS',
    17: 'UDP',
    18: 'MUX',
    19: 'DCN-MEAS',
    20: 'HMP',
    21: 'PRM',
    22: 'XNS-IDP',
    23: 'TRUNK-1',
    24: 'TRUNK-2',
    25: 'LEAF-1',
    26: 'LEAF-2',
    27: 'RDP',
    28: 'IRTP',
    29: 'ISO-TP4',
    30: 'NETBLT',
    31: 'MFE-NSP',
    32: 'MERIT-INP',
    33: 'DCCP',
    34: '3PC',
    35: 'IDPR',
    36: 'XTP',
    37: 'DDP',
    38: 'IDPR-CMTP',
    39: 'TP++',
    40: 'IL',
    41: 'IPv6',
    42: 'SDRP',
    43: 'IPv6-Route',
    44: 'IPv6-Frag',
    45: 'IDRP',
    46: 'RSVP',
    47: 'GRE',
    48: 'DSR',
    49: 'BNA',
    50: 'ESP',
    51: 'AH',
    52: 'I-NLSP',
    53: 'SWIPE (deprecated)',
    54: 'NARP',
    55: 'MOBILE',
    56: 'TLSP',
    57: 'SKIP',
    58: 'IPv6-ICMP',
    59: 'IPv6-NoNxt',
    60: 'IPv6-Opts',
    62: 'CFTP',
    64: 'SAT-EXPAK',
    65: 'KRYPTOLAN',
    66: 'RVD',
    67: 'IPPC',
    69: 'SAT-MON',
    70: 'VISA',
    71: 'IPCV',
    72: 'CPNX',
    73: 'CPHB',
    74: 'WSN',
    75: 'PVP',
    76: 'BR-SAT-MON',
    77: 'SUN-ND',
    78: 'WB-MON',
    79: 'WB-EXPAK',
    80: 'ISO-IP',
    81: 'VMTP',
    82: 'SECURE-VMTP',
    83: 'VINES',
    84: 'TTP',
    84: 'IPTM',
    85: 'NSFNET-IGP',
    86: 'DGP',
    87: 'TCF',
    88: 'EIGRP',
    89: 'OSPFIGP',
    90: 'Sprite-RPC',
    91: 'LARP',
    92: 'MTP',
    93: 'AX.25',
    94: 'IPIP',
    95: 'MICP (deprecated)',
    96: 'SCC-SP',
    97: 'ETHERIP',
    98: 'ENCAP',
    100: 'GMTP',
    101: 'IFMP',
    102: 'PNNI',
    103: 'PIM',
    104: 'ARIS',
    105: 'SCPS',
    106: 'QNX',
    107: 'A/N',
    108: 'IPComp',
    109: 'SNP',
    110: 'Compaq-Peer',
    111: 'IPX-in-IP',
    112: 'VRRP',
    113: 'PGM',
    115: 'L2TP',
    116: 'DDX',
    117: 'IATP',
    118: 'STP',
    119: 'SRP',
    120: 'UTI',
    121: 'SMP',
    122: 'SM',
    123: 'PTP',
    124: 'ISIS over IPv4',
    125: 'FIRE',
    126: 'CRTP',
    127: 'CRUDP',
    128: 'SSCOPMCE',
    129: 'IPLT',
    130: 'SPS',
    131: 'PIPE',
    132: 'SCTP',
    133: 'FC',
    134: 'RSVP-E2E-IGNORE',
    135: 'Mobility Header',
    136: 'UDPLite',
    137: 'MPLS-in-IP',
    138: 'manet',
    139: 'HIP',
    140: 'Shim6',
    141: 'WESP',
    142: 'ROHC'
}

class Packet(object):
    #Base Class for all Packets

    @abstractmethod
    def get_header_len(self):
        pass

    @abstractmethod
    def get_data_len(self):
        pass

class TransportLayerPacket(Packet):
    #Base class packets at the transport layer.
    @abstractmethod
    def get_body(self):
        pass

class IPPacket(Packet):
    # Base class for all packets.
    def __init__(self, buf):
        # Creates packet from raw data.
        self.buf = buf
        self._src_ip = socket.inet_ntoa(buf[12:16])
        self._dst_ip = socket.inet_ntoa(buf[16:20])
        self._ihl = (unpack('!B', buf[0:1])[0] & 0xF) * 4
        self._proto = unpack('!B', buf[9:10])[0]
        self._payload = payload_builder(buf[self._ihl:], self._proto)

    def get_src_ip(self):
        return self._src_ip

    def get_dst_ip(self):
        return self._dst_ip

    def get_protocol(self):
        return self._proto

    def get_payload(self):
        return self._payload

    def get_header_len(self):
        return self._ihl

    def get_data_len(self):
        return len(self.buf) - self._ihl

    def __str__(self):
        return f'IP Packet {self._src_ip} => {self._dst_ip}, proto={proto_to_string(self._proto)}'

class TCPPacket(TransportLayerPacket):
    #TCP Packet Object
    def __init__(self, buff):
        self._parse_header(buff)

    def _parse_header(self, buff):
        header_fields = unpack('!HHIIHHHH', buff[:20])
        self._src_port, self._dst_port, self._seq_num, self._ack_num, flags, self._win_size, self._checksum, self._urg_ptr = header_fields
        #parse Flags
        self.flag_ns = bool(flags & 0x0100)
        self.flag.cwr = bool(flags & 0x0080)
        self.flag_ece = bool(flags & 0x0040)
        self.flag_urg = bool(flags & 0x0020)
        self.flag_ack = bool(flags & 0x0010)
        self.flag_psh = bool(flags & 0x0008)
        self.flag_rst = bool(flags & 0x0004)
        self.flag_syn = bool(flags & 0x0002)
        self.flag_fin = bool(flags & 0x0001)
        # can be parsed later if we care:
        #self._options = buff[20:(self._data_offset * 4)]
        #self._total_length = len(buff)
        #self._body = buff[self.get_header_len():]

    def get_header_len(self):
        return self._data_offset * 4

    def get_data_len(self):
        return len(self.buf) - self.get_header_len()

    def get_src_port(self):
        return self._src_port
    
    def get_dst_port(self):
        return self._dst_port
    
    def get_body(self):
        return str(self._body)
    
    def __unicode__(self):
        #Returns a printable version of the TCP header
        return u'TCP from %d to %d' % (self._src_port, self._dst_port)

class UDPPacket(TransportLayerPacket):
    #UDP Packet Object

    def __init__(self, buff):
        self._parse_header(buff)

    def _parse_header(self, buff):
        # Unpack source port, destination port, length, and checksum.
        header_fields = unpack('!HHHH', buff[:8])
        self._src_port, self._dst_port, self._length, self._checksum = header_fields

    def get_header_len(self):
        return 8

    def get_data_len(self):
        return len(self.buf) - self.get_header_len()

    def get_src_port(self):
        return self._src_port

    def get_dst_port(self):
        return self._dst_port

    def get_body(self):
        return str(self._body)
    
    def __unicode__(self):
        #Returns a Printable Version Of UDP Header
        return u'UDP from %d to %d' % (self._src_port, self._dst_port)

def payload_builder(payload_buff, protocol):
    #If `protocol` is supported, builds packet object from buff
    if protocol == socket.IPPROTO_TCP:
        return TCPPacket(payload_buff)
    elif protocol == socket.IPPROTO_UDP:
        return UDPPacket(payload_buff)
    else:
        return None

def to_tuple(ippacket, flip=False):
    #Create a tuple from a TCP packet.
    #The flip argument flips the source and destination port, so that they will
    #be consistent between ingress and egress.
    payload = ippacket.get_payload()
    if isinstance(payload, TCPPacket):
        if flip:
            return (ippacket.get_dst_ip(), payload.get_dst_port(),  # remote
                    ippacket.get_src_ip(), payload.get_src_port())  # local
        else:
            return (ippacket.get_src_ip(), payload.get_src_port(),  # remote
                    ippacket.get_dst_ip(), payload.get_dst_port())  # local
    return None


def proto_to_string(proto):
    #Convert protocol number to a string
    return PROTO_NUMS.get(proto, 'unknown')
