class IoTDevice:
    # Is it better to have a class for a device packet structure, 
    # because that way we can whitelist/blacklist by port, protocol, etc
    # and not only by IP and MAC?
    def __init__(self, ip, mac_address):
        self.name: str = mac_address
        self.ip = ip
        self.mac_address = mac_address

        # Is there a difference between protocols and ports?
        self.ports = []
        self.protocols = []

        self.white_list = []
        self.black_list = []

    def add_port(self, port):
        self.ports.append(port)

    def remove_port(self, port):
        self.ports.remove(port)

    def change_name(self, name):
        self.name = name

    def add_to_white_list(self, ip):
        self.white_list.append(ip)

    def remove_from_white_list(self, ip):
        self.white_list.remove(ip)

    def add_to_black_list(self, ip):
        self.black_list.append(ip)
    
    def remove_from_black_list(self, ip):
        self.black_list.remove(ip)
    


    def __str__(self):
        return f'IP: {self.ip}, MAC: {self.mac_address}'
