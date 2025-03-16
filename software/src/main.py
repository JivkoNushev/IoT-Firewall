import threading

from core.firewall import Firewall, run_firewall
from core.database import Database, run_database


if __name__ == '__main__':
    database = Database("localhost", "firewall_user", "password", "firewall_db")
    database_thread = threading.Thread(target=run_database, args=(database,))

    firewall = Firewall()
    firewall_thread = threading.Thread(target=run_firewall, args=(firewall,))
    

    database_thread.start()
    firewall_thread.start()


    firewall_thread.join() 

    database_thread.join()
