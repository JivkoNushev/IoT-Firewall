from datetime import timedelta

INTERFACE: str = 'wlan0'
SNIFF_TIMEOUT_SEC: int = 10
GRACE_PERIOD: timedelta = timedelta(minutes=5)
LAN_SUBNET: str = '192.168.1.0/24'