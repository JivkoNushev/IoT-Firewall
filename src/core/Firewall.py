import pyshark

from .firewall_config import INTERFACE, SNIFF_TIMEOUT_SEC

class Rule:
    def __init__(self):
        pass

class Firewall:
    def __init__(self):
        capture = pyshark.LiveCapture(interface=INTERFACE)
        capture.sniff(timeout=SNIFF_TIMEOUT_SEC)

    def run(self):
        pass

    def add_rule(self, rule):
        pass

    def remove_rule(self, rule):
        pass
