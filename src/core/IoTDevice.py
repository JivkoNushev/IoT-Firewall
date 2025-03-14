class IoTDevice:

    def __init__(self, name, ip, mac_address):
        self.name = name
        self.ip = ip
        self.mac_address = mac_address

        self.ports = []

    def add_port(self, port):
        self.ports.append(port)

    def __str__(self):
        return f'IP: {self.ip}, MAC: {self.mac_address}'
