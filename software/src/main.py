import threading

from core.Firewall import Firewall

if __name__ == '__main__':
    Firewall = Firewall()

    firewall_thread = threading.Thread(target=Firewall.run)
    firewall_thread.start()

    thread.join()

