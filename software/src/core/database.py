import queue
import sqlite3

from ..main import thread_safe_queue

class Database:
    def __init__(self, db):
        _conn = sqlite3.connect("database.db")
        _cursor = _conn.cursor()

        _cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='Logs'
        """)
        if not _cursor.fetchall():
            self._create_tables()

    def run(self):
        while True:
            if thread_safe_queue.not_empty():
                packet = thread_safe_queue.get()

                stripped_packet = self._strip_packet(packet)
                self._commit_stripped_packet(stripped_packet)

    def _create_tables(self):
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_src TEXT NOT NULL,
                ip_dst TEXT NOT NULL,
                mac_src TEXT NOT NULL,
                mac_dst TEXT NOT NULL,
                port INTEGER NOT NULL,
                protocol TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._conn.commit()

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ip TEXT NOT NULL,
                mac_address TEXT NOT NULL,
                is_quarantined INTEGER NOT NULL CHECK (is_quarantined IN (0, 1)),
                logs_id INTEGER,
                FOREIGN KEY (logs_id) REFERENCES Logs(id) ON DELETE SET NULL
            )
        """)
        self._conn.commit()

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Device_Ports (
                device_id INTEGER NOT NULL,
                port INTEGER NOT NULL,
                protocol TEXT NOT NULL,
                FOREIGN KEY (device_id) REFERENCES Devices(id) ON DELETE CASCADE
            )
        """)
        self._conn.commit()

    def _strip_packet(self, packet):
        pass

    def _commit_stripped_packet(self, stripped_packet):
        with self._conn:
            # Insert log entry
            self._cursor.execute("""
                INSERT INTO Logs (ip_src, ip_dst, mac_src, mac_dst, port, protocol) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                stripped_packet.ip_src,
                stripped_packet.ip_dst,
                stripped_packet.mac_src,
                stripped_packet.mac_dst,
                stripped_packet.port,
                stripped_packet.protocol
            ))
            
            log_id = self._cursor.lastrowid  # Get the inserted log ID

            # Check if the device already exists
            self._cursor.execute("""
                SELECT id FROM Devices WHERE mac_address = ?
            """, (stripped_packet.mac_src,))
            device = self._cursor.fetchone()

            if device:
                device_id = device[0]
                # Update device with latest log ID
                self._cursor.execute("""
                    UPDATE Devices SET logs_id = ? WHERE id = ?
                """, (log_id, device_id))
            else:
                # If the device does not exist, insert it
                self._cursor.execute("""
                    INSERT INTO Devices (name, ip, mac_address, is_quarantined, logs_id) 
                    VALUES (?, ?, ?, ?, ?)
                """, ("Unknown Device", stripped_packet.ip_src, stripped_packet.mac_src, 0, log_id))
                device_id = self._cursor.lastrowid  # Get the new device ID

            # Insert the port & protocol into Device_Ports
            self._cursor.execute("""
                INSERT INTO Device_Ports (device_id, port, protocol) 
                VALUES (?, ?, ?)
            """, (device_id, stripped_packet.port, stripped_packet.protocol))
