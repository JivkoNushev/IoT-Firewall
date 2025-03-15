import subprocess
import pyshark

from .firewall_config import INTERFACE, SNIFF_TIMEOUT_SEC
from .IoTDevice import IoTDevice

class Rule:
    def __init__(self):
        # subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "80", "-j", "ACCEPT"])
        pass

class Firewall:
    def __init__(self):
        capture = pyshark.LiveCapture(interface=INTERFACE)
        capture.sniff(timeout=SNIFF_TIMEOUT_SEC)

        known_devices: IoTDevice = []
    
    def run(self):
        for packet in self.capture.sniff_continuously():
            # Get the device if exists, if not create a new one
            device = self._get_device(packet)

            if(self.packet_is_malicious(packet, device)):
                self.quarantine_device(device)
            
            self._save_packet_info(packet)

    def get_known_devices_src_ips(self):
        return [device.ip for device in self.known_devices]
    
    def packet_is_malicious(self, packet, device):
        # Do some heuristic checks
        pass

    def quarantine_device(self, device):
        # Block all incoming and outgoing traffic
        # Block traffic to all devices that are WhiteListed by the device
        pass

    # Maybe whitelist not only by IP but also by Port and Protocol
    def whitelist_device(self, device, ip):
        pass

    # Maybe blacklist not only by IP but also by Port and Protocol
    def blacklist_device(self, device, ip):
        pass

    def _get_device(self, packet):
        known_devices_src_ips = self.get_known_devices_src_ips()

        # If exists in known devices return it
        if packet.ip.src in known_devices_src_ips:
            return self.known_devices[known_devices_src_ips.index(packet.ip.src)]
        
        # If not, create a new device and return it
        device = IoTDevice(packet.ip.src, packet.eth.src)
        self.known_devices.append(device)

        return  

    def _save_packet_info(self, packet):
        # Save needed packet info to a database
        pass

    def _add_rule(self, rule):
        pass

    def _remove_rule(self, rule):
        pass