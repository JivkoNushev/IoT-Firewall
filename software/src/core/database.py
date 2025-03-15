import mysql.connector
from mysql.connector import Error

import queue

thread_safe_queue = queue.Queue()

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
            if thread_safe_queue.not_empty():
                packet = thread_safe_queue.get()
                stripped_packet = self._strip_packet(packet)
                self._commit_stripped_packet(stripped_packet)

    def _create_tables(self):
        try:
            # Create Logs table
            self._cursor.execute("""
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
                    is_quarantined TINYINT(1) NOT NULL DEFAULT 0,
                    logs_id INT,
                    FOREIGN KEY (logs_id) REFERENCES Logs(id) ON DELETE SET NULL
                ) ENGINE=InnoDB
            """)

            # Create Device_Ports table
            self._cursor.execute("""
                CREATE TABLE Device_Ports (
                    device_id INT NOT NULL,
                    port INT NOT NULL,
                    protocol VARCHAR(20) NOT NULL,
                    FOREIGN KEY (device_id) REFERENCES Devices(id) ON DELETE CASCADE,
                    INDEX composite_idx (device_id, port, protocol)
                ) ENGINE=InnoDB
            """)

            self._conn.commit()
        except Error as e:
            print(f"Table creation error: {e}")
            self._conn.rollback()
            raise

    def _strip_packet(self, packet):
        # Implement your packet stripping logic here
        return packet  # Return structured data

    def _commit_stripped_packet(self, stripped_packet):
        try:
            # Insert log entry
            self._cursor.execute("""
                INSERT INTO Logs (ip_src, ip_dst, mac_src, mac_dst, port, protocol) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                stripped_packet.ip_src,
                stripped_packet.ip_dst,
                stripped_packet.mac_src,
                stripped_packet.mac_dst,
                stripped_packet.port,
                stripped_packet.protocol
            ))
            
            log_id = self._cursor.lastrowid

            # Upsert device information
            self._cursor.execute("""
                INSERT INTO Devices (name, ip, mac_address, is_quarantined, logs_id)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    ip = VALUES(ip),
                    logs_id = VALUES(logs_id)
            """, (
                "Unknown Device",
                stripped_packet.ip_src,
                stripped_packet.mac_src,
                0,
                log_id
            ))

            device_id = self._cursor.lastrowid
            if device_id == 0:  # If existing record was updated
                self._cursor.execute("""
                    SELECT id FROM Devices WHERE mac_address = %s
                """, (stripped_packet.mac_src,))
                device_id = self._cursor.fetchone()[0]

            # Insert port information
            self._cursor.execute("""
                INSERT INTO Device_Ports (device_id, port, protocol)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    port = VALUES(port),
                    protocol = VALUES(protocol)
            """, (device_id, stripped_packet.port, stripped_packet.protocol))

            self._conn.commit()

        except Error as e:
            print(f"Commit error: {e}")
            self._conn.rollback()
            raise

    def __del__(self):
        if hasattr(self, '_conn') and self._conn.is_connected():
            self._cursor.close()
            self._conn.close()