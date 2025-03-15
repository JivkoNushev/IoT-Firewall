import threading
import queue

from core.firewall import Firewall
from core.database import Database

if __name__ == '__main__':
    database = Database("localhost", "firewall_user", "password", "firewall_db")
    database_thread = threading.Thread(target=Database.run)

    firewall = Firewall()
    firewall_thread = threading.Thread(target=Firewall.run)
    

    database_thread.start()
    firewall_thread.start()


    firewall_thread.join() 

    database_thread.join()
