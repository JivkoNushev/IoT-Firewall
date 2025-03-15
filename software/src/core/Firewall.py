import datetime
import subprocess
import pyshark
import iptc

from .firewall_config import INTERFACE, SNIFF_TIMEOUT_SEC
from .IoTDevice import IoTDevice

class Firewall:
    def __init__(self):
        capture = pyshark.LiveCapture(interface=INTERFACE)
        capture.sniff(timeout=SNIFF_TIMEOUT_SEC)

        self.start_time = datetime.now()

        known_devices: IoTDevice = []
    
    def run(self):
        for packet in self.capture.sniff_continuously():
            if self._in_grace_period(self):
                self._save_device(packet)
            elif self.packet_is_malicious(packet):
                self.quarantine_devices_from_packet(packet)

            self._save_packet_info(packet)

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
        
        return False

    def quarantine_device(self, device):
        # Block all incoming and outgoing traffic
        # Block traffic to all devices that are WhiteListed by the device
        if device.is_quarantined:
            return

        pass

    # Maybe whitelist not only by IP but also by Port and Protocol
    def whitelist_device(self, device, ip):
        pass

    # Maybe blacklist not only by IP but also by Port and Protocol
    def blacklist_device(self, device, ip):
        pass

    def _get_device_from_ip(self, ip):
        for device in self.known_devices:
            if device.ip == ip:
                return device
        return None

    def _save_device(self, packet):
        device = self._get_device_from_ip(packet.ip.src)
        if device is None:
            device = IoTDevice(packet)
            self.known_devices.append(device)
        else:
            device._update_from_packet(packet)
    
    def _in_grace_period(self):
        self.now = datetime.now()
        if self.now - self.start_time < self.grace_period:
            return True
        
        return False

    def _save_packet_info(self, packet):
        # Save needed packet info to a database
        pass

    def _add_rule(self, rule: Rule):
        pass

    def _remove_rule(self, rule):
        pass