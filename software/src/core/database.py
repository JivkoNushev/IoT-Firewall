import mysql.connector
from mysql.connector import Error

import queue
from .IoTDevice import IoTDevice
from typing import List

thread_safe_queue_logs = queue.Queue()
thread_safe_queue_devices = queue.Queue()
thread_safe_queue_whitelists = queue.Queue()

thread_safe_queue_put_devices = queue.Queue()
thread_safe_queue_get_devices = queue.Queue()


def run_database(self):
        while True:
            if not thread_safe_queue_logs.empty():
                log = thread_safe_queue_logs.get()
                self._commit_log(log)

            if not thread_safe_queue_devices.empty():
                device = thread_safe_queue_devices.get()
                self._commit_device(device)

            if not thread_safe_queue_whitelists.empty():
                whitelist = thread_safe_queue_whitelists.get()
                self._commit_whitelist(whitelist)
            
            if not thread_safe_queue_get_devices.empty():
                thread_safe_queue_get_devices.get()
                thread_safe_queue_put_devices.put(self._get_devices())

class Database:
    def __init__(self, host, user, password, database):
        try:
            self._conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self._cursor = self._conn.cursor()
            
            # self._cursor.execute("SHOW TABLES LIKE 'Logs'")
            self._create_tables()
                
        except Error as e:
            print(f"Database connection error: {e}")
            
    def _create_tables(self):
        try:
            # Create Logs table
            self._cursor.execute("""    

                CREATE TABLE IF NOT EXISTS Logs (
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
                CREATE TABLE IF NOT EXISTS Devices (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    ip VARCHAR(45) NOT NULL UNIQUE,
                    mac_address VARCHAR(17) NOT NULL UNIQUE,
                    port INT NOT NULL,
                    protocol VARCHAR(20) NOT NULL,
                    is_quarantined TINYINT(1) NOT NULL DEFAULT 0,
                    logs_id INT,
                    FOREIGN KEY (logs_id) REFERENCES Logs(id) ON DELETE SET NULL
                ) ENGINE=InnoDB# parse to Device objects
        return self._cursor.fetchall()
            """)

            #Whitelist
            # TODO: flag is device is not whitelisted?
            self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS Whitelist (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    whitelisted_ip VARCHAR(45) NOT NULL UNIQUE,
                    device_id INT NOT NULL DEFAULT 0,
                    FOREIGN KEY (device_id) REFERENCES Devices(id)
                ) ENGINE=InnoDB
            """)

            self._conn.commit()
        except Error as e:
            print(f"Table creation error: {e}")

    def _get_devices(self):
        self._cursor.execute("SELECT * FROM Devices")
        devices: List[IoTDevice] = []
        for device in self._cursor.fetchall():
            self._cursor.execute("SELECT * FROM Whitelist WHERE device_id = %s", (device['id'],))
            whitelist = [whitelisted['whitelisted_ip'] for whitelisted in self._cursor.fetchall()]
            devices.append(IoTDevice(device['name'], device['ip'], device['mac_address'], device['port'], device['protocol'], device['is_quarantined'], whitelist))
        return devices


# CHANGE HERE
    def _commit_log(self, log):
        try:
            self._cursor.execute("""
                INSERT INTO Logs (ip_src, ip_dst, mac_src, mac_dst, port, protocol)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (log['ip_src'], log['ip_dst'], log['mac_src'], log['mac_dst'], log['port'], log['protocol']))
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
                    VALUES (%s, %s, %s, %s, %s, %s)
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