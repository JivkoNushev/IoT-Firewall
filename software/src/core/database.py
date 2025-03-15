import mysql.connector
from mysql.connector import Error

import queue

thread_safe_queue_logs = queue.Queue()
thread_safe_queue_devices = queue.Queue()
thread_safe_queue_whitelists = queue.Queue()

class Database:
    def __init__(self, host, user, password, database):
        try:
            # Establish database connection
            self._conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self._cursor = self._conn.cursor()
            
            # Check if tables exist
            self._cursor.execute("SHOW TABLES LIKE 'Logs'")
            if not self._cursor.fetchall():
                self._create_tables()
                
        except Error as e:
            print(f"Database connection error: {e}")
            raise

    def run(self):
        while True:
            if thread_safe_queue_logs.not_empty():
                log = thread_safe_queue_logs.get()
                self._commit_log(log)

            if thread_safe_queue_devices.not_empty():
                device = thread_safe_queue_devices.get()
                self._commit_device(device)

            if thread_safe_queue_whitelists.not_empty():
                whitelist = thread_safe_queue_whitelists.get()
                self._commit_whitelist(whitelist)

    def _create_tables(self):
        try:
            # Create Logs table
            self._cursor.execute("""            self._conn.commit()

                CREATE TABLE Logs (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    ip_src VARCHAR(45) NOT NULL,
                    ip_dst VARCHAR(45) NOT NULL,
                    mac_src VARCHAR(17) NOT NULL,
                    mac_dst VARCHAR(17) NOT NULL,
                    port INT NOT NULL,
                    protocol VARCHAR(20) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB
            """)

            # Create Devices table
            self._cursor.execute("""
                CREATE TABLE Devices (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    ip VARCHAR(45) NOT NULL,
                    mac_address VARCHAR(17) NOT NULL UNIQUE,
                    port INT NOT NULL,
                    protocol VARCHAR(20) NOT NULL,
                    is_quarantined TINYINT(1) NOT NULL DEFAULT 0,
                    logs_id INT,
                    FOREIGN KEY (logs_id) REFERENCES Logs(id) ON DELETE SET NULL
                ) ENGINE=InnoDB
            """)

            #Whitelist
            self._cursor.execute("""
                CREATE TABLE Whitelist (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    ip VARCHAR(45) NOT NULL,
                    whitelisted_ip TINYINT(1) NOT NULL DEFAULT 0,
                    FOREIGN KEY (id) REFERENCES Devices(id)
                ) ENGINE=InnoDB
            """)

            self._conn.commit()
        except Error as e:
            print(f"Table creation error: {e}")
            self._conn.rollback()
            raise

    def _commit_log(self, log):
        try:
            self._cursor.execute("""
                INSERT INTO Logs (ip_src, ip_dst, mac_src, mac_dst, port, protocol)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (log.ip_src, log.ip_dst, log.mac_src, log.mac_dst, log.port, log.protocol))
            self._conn.commit()
        except Error as e:
            print(f"Log commit error: {e}")
            self._conn.rollback()
            raise
    
    def _commit_device(self, device):
        try:
            # if exists remove it if not insert it
            self._cursor.execute("SELECT * FROM Devices WHERE ip = %s", (device.ip,))
            if self._cursor.fetchall():
                self._cursor.execute("DELETE FROM Devices WHERE ip = %s", (device.ip,))
            else:
                self._cursor.execute("""
                    INSERT INTO Devices (name, ip, mac_address, port, protocol, is_quarantined)
                    VALUES (%s, %s, %s, %s)
                """, (device.name, device.ip, device.mac_address, device.port, device.protocol, device.is_quarantined))
            self._conn.commit()
        except Error as e:
            print(f"Device commit error: {e}")
            self._conn.rollback()
            raise
    
    def _commit_whitelist(self, src_dst):
        try:
            src, dst = src_dst

            self._cursor.execute("SELECT * FROM Whitelist WHERE ip = %s AND whitelisted_ip = %s", (src, dst))
            if self._cursor.fetchall():
                self._cursor.execute("DELETE FROM Whitelist WHERE ip = %s AND whitelisted_ip = %s", (src, dst))
            else:
                self._cursor.execute("INSERT INTO Whitelist (ip, whitelisted_ip) VALUES (%s, %s)", (src, dst))
            self._conn.commit()
        except Error as e:
            print(f"Whitelist commit error: {e}")
            self._conn.rollback()
            raise

    def __del__(self):
        if hasattr(self, '_conn') and self._conn.is_connected():
            self._cursor.close()
            self._conn.close()