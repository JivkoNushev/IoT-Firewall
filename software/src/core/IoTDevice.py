import iptc
from software.firewall_config import INTERFACE, SNIFF_TIMEOUT_SEC

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


    def _update_from_packet(self, packet):
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

    def add_to_black_list(self, ip):
        self.black_list.append(ip)
    
    def remove_from_black_list(self, ip):
        self.black_list.remove(ip)

    def _block_traffic(self, direction):
        if direction.upper() != 'INPUT' and direction.upper() != 'OUTPUT':
            print('Invalid direction')
            return

        for ip in [device.ip for device in self.whitelist]:
            rule = iptc.Rule()
            
            if direction.upper() == 'INPUT':
                rule.in_interface = INTERFACE
                rule.src = ip
            else:  # OUTPUT
                rule.out_interface = INTERFACE
                rule.dst = ip
            
        target = iptc.Target(rule, "ACCEPT")
        rule.target = target
        chain.insert_rule(rule)  # Insert at beginning to ensure priority

        
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), direction.upper())
        rule = iptc.Rule()
        rule.in_interface = INTERFACE
        rule.src = self.ip
        rule.target = iptc.Target(rule, 'DROP')
        chain.insert_rule(rule)
        
    
    def _unblock_traffic(self, direction):
        if direction.upper() != 'INPUT' and direction.upper() != 'OUTPUT':
            print('Invalid direction')
            return

        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), direction.upper())
        rule = iptc.Rule()
        rule.in_interface = INTERFACE
        rule.src = self.ip
        rule.target = iptc.Target(rule, 'ACCEPT')
        chain.insert_rule(rule)

    def _block_all_traffic(self, keep_whitelisted: bool = True):
        # remove all rules
        self._block_traffic('INPUT')
        self._block_traffic('OUTPUT')

    def _unblock_all_traffic(self):
        self._unblock_traffic('INPUT')
        self._unblock_traffic('OUTPUT')

    def _block_traffic_to(self, ip):
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), 'OUTPUT')
        rule = iptc.Rule()
        rule.in_interface = INTERFACE
        rule.dst = ip
        rule.target = iptc.Target(rule, 'DROP')
        chain.insert_rule(rule)
    
    def _unblock_traffic_to(self, ip):
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), 'OUTPUT')
        rule = iptc.Rule()
        rule.in_interface = INTERFACE
        rule.dst = ip
        rule.target = iptc.Target(rule, 'ACCEPT')
        chain.insert_rule(rule)

    def _block_traffic_from(self, ip):
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), 'INPUT')
        rule = iptc.Rule()
        rule.in_interface = INTERFACE
        rule.src = ip
        rule.target = iptc.Target(rule, 'DROP')
        chain.insert_rule(rule)
    
    def _unblock_traffic_from(self, ip):
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), 'INPUT')
        rule = iptc.Rule()
        rule.in_interface = INTERFACE
        rule.src = ip
        rule.target = iptc.Target(rule, 'ACCEPT')
        chain.insert_rule(rule)

    def __str__(self):
        return f'IP: {self.ip}, MAC: {self.mac_address}'
