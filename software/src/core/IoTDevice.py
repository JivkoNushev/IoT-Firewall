import iptc

from .firewall_config import INTERFACE, SNIFF_TIMEOUT_SEC, GRACE_PERIOD, LAN_SUBNET

class IoTDevice:
    # Is it better to have a class for a device packet structure, 
    # because that way we can whitelist/blacklist by port, protocol, etc
    # and not only by IP and MAC?
    def __init__(self, packet):
        self.name: str = packet.ip.src
        self.ip = packet.ip.src
        self.mac_address = packet.eth.src

        # Is there a difference between protocols and ports?
        self.ports = []
        self.protocols = []

        self.whitelist = []

        self.rules = []

        self.is_quarantined = False

    def __init__(self, name, ip, mac_address, port, protocol, is_quarantined, whitelist):
        self.name = name

        self.ip = ip

        self.mac_address = mac_address

        self.ports = []
        self.ports.append(port)

        self.protocols = []
        self.protocols.append(protocol)

        self.whitelist = whitelist

        self.rules = []

        self.is_quarantined = is_quarantined


    def update_from_packet(self, packet):
        if packet.port not in self.ports:
            self.ports.append(packet.port)
        if packet.protocol not in self.protocols:
            self.protocols.append(packet.protocol)
        
    def add_port(self, port):
        self.ports.append(port)

    def remove_port(self, port):
        self.ports.remove(port)

    def change_name(self, name):
        self.name = name

    def add_to_whitelist(self, ip):
        self.whitelist.append(ip)

    def remove_from_whitelist(self, ip):
        self.whitelist.remove(ip)

    def __str__(self):
        return f'IP: {self.ip}, MAC: {self.mac_address}'
