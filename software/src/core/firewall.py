import datetime
import ipaddress
from typing import List
import pyshark
import iptc


from ...firewall_config import INTERFACE, SNIFF_TIMEOUT_SEC, GRACE_PERIOD, LAN_SUBNET
from .IoTDevice import IoTDevice

from ..main import thread_safe_queue

class Firewall:
    def __init__(self):

        self._start_time = datetime.now()
        self._grace_period = GRACE_PERIOD
        self._grace_period_ended = False
        self._blocked_all_traffic = False

        self._table = iptc.Table(iptc.Table.FILTER)
        self._input_chain = iptc.Chain(self.filter_table, "INPUT")
        self._output_chain = iptc.Chain(self.filter_table, "OUTPUT")
        self._known_devices: List[IoTDevice] = []

        self._valid_mac_addresses = []
        with open('../mac_address_vendors.txt', 'r') as file:
            for line in file:
                mac = line.strip()
                if mac:
                    self._valid_mac_addresses.append(mac)

        capture = pyshark.LiveCapture(interface=INTERFACE)
        capture.sniff(timeout=SNIFF_TIMEOUT_SEC)
    
    def run(self):
        for packet in self.capture.sniff_continuously():
            if self._in_grace_period(self):
                if self._is_ip_in_lan(packet.ip.src) and self._is_valid_mac_address(packet.eth.src):
                    self._save_device(packet)
            else:
                if not self._blocked_all_traffic:
                    for device in self.known_devices:
                        self._block_all_traffic(device)
                    self._blocked_all_traffic = True

                if self.packet_is_malicious(packet):
                    self.quarantine_devices_from_packet(packet)

            self._save_packet_info(packet)
    
    def _get_chain(self, direction: str) -> iptc.Chain:
        return self._input_chain if direction == "INPUT" else self._output_chain
    
    def _block_traffic_in_direction(self, device: IoTDevice, direction: str, keep_whitelisted: bool):
        chain = self._get_chain(direction)
        chain.flush()
        
        if keep_whitelisted:
            for ip in device.whitelist:
                accept_rule = iptc.Rule()
            
                if direction == "INPUT":
                    accept_rule.in_interface = self.interface
                    accept_rule.src = ip
                    accept_rule.dst = device.ip
                elif direction == "OUTPUT":
                    accept_rule.out_interface = self.interface
                    accept_rule.src = device.ip
                    accept_rule.dst = ip
                else:
                    accept_rule = None
                    
                if accept_rule is not None:
                    accept_rule.target = iptc.Target(accept_rule, "ACCEPT")
                    chain.insert_rule(accept_rule)
                else:
                    print("Could not create accept rule for IP: " + ip)
                    return

        block_rule = iptc.Rule()
        
        if direction == "INPUT":
            block_rule.in_interface = self.interface
            block_rule.dst = device.ip
        elif direction == "OUTPUT":
            block_rule.out_interface = self.interface
            block_rule.src = device.ip
        else:
            block_rule = None
            
        if block_rule is not None:
            block_rule.target = iptc.Target(block_rule, "DROP")
            chain.insert_rule(block_rule)
        else:
            print("Could not create block rule for IP: " + ip)
            return 
        
        if block_rule is not None:
            chain.append_rule(block_rule)
        else:
            print("Could not create block rule for device with IP: " + device.ip)

        self._table.commit()
    

    def _block_all_traffic(self, device: IoTDevice, keep_whitelisted: bool = True):
        self._block_traffic_in_direction(device, "INPUT", keep_whitelisted)
        self._block_traffic_in_direction(device, "OUTPUT", keep_whitelisted)
      
    def get_known_devices_src_ips(self):
        return [device.ip for device in self.known_devices]
    
    def quarantine_devices_from_packet(self, packet):
        initiator = self._get_device_from_ip(packet.ip.src)
        responder = self._get_device_from_ip(packet.ip.dest)

        if initiator is not None:
            self.quarantine_device(initiator)
        if responder is not None:
            self.quarantine_device(responder)

    def packet_is_malicious(self, packet):
        initiator = self._get_device_from_ip(packet.ip.src)

        if initiator is None: # then device is a server
            device = self._get_device_from_ip(packet.ip.dest)
            if device is None or device.is_quarantined or not device.white_listed.contains(packet.ip.src):
                return True
        elif initiator.is_quarantined or not initiator.white_listed.contains(packet.ip.dest):
                return True    
        
        # Huristic checks
        if packet.port not in initiator.ports:
            return True
        
        if packet.protocol not in initiator.protocols:
            return True

        return False

    def quarantine_device(self, device):
        if device.is_quarantined:
            return
        
        self._block_all_traffic(device, False)

        device.is_quarantined = True

    def _get_device_from_ip(self, ip):
        for device in self._known_devices:
            if device.ip == ip:
                return device
        return None
    
    def _is_ip_in_lan(ip_str):
        try:
            ip = ipaddress.ip_address(ip_str)

            if ip.is_private:
                your_subnet = ipaddress.ip_network(LAN_SUBNET) 
                return ip in your_subnet
            return False
        except ValueError:
            return False


    def _is_valid_mac_address(self, mac):
        src_mac = mac.replace(':', '')
        oui = src_mac[:6].upper()
        return oui in self._valid_mac_addresses

    def _get_device(self, packet):
        if packet.ip.src in self._known_devices:
            device = self._known_devices[(self.get_known_devices_src_ips().index(packet.ip.src))]
            device.update_from_packet(packet)
            return device
        else: return None


    def _save_device(self, packet):
        device = self._get_device(packet)
        if device is None:
            device = IoTDevice(packet)
            self._known_devices.append(device)
        else:
            device.update_from_packet(packet)

    def _in_grace_period(self):
        self._grace_period_ended = datetime.now() - self._start_time >= self._grace_period
        
        return self._grace_period_ended

    def _add_rule(self, rule):
        pass

    def _remove_rule(self, rule):
        pass

    def add_whitelisted(self, ips: List[str]):
        pass

    def remove_whitelisted(self, ips: List[str]):
        pass

    def _save_packet_info(self, packet):
        thread_safe_queue.put(packet)
