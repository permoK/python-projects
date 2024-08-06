import sqlite3
import datetime
import subprocess
import re

class NetworkHistoryTracker:
    def __init__(self, db_name='network_history.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_history (
            id INTEGER PRIMARY KEY,
            ip_address TEXT,
            mac_address TEXT,
            timestamp DATETIME,
            device_name TEXT
        )
        ''')
        self.conn.commit()

    def capture_arp_cache(self):
        arp_output = subprocess.check_output(["arp", "-e"]).decode('utf-8')
        lines = arp_output.split('\n')[1:]  # Skip the header line
        for line in lines:
            if line.strip():
                parts = re.split(r'\s+', line.strip())
                if len(parts) >= 4:
                    ip_address = parts[0]
                    mac_address = parts[2]
                    self.store_device_info(ip_address, mac_address)

    def store_device_info(self, ip_address, mac_address, device_name=None):
        cursor = self.conn.cursor()
        timestamp = datetime.datetime.now()
        cursor.execute('''
        INSERT INTO device_history (ip_address, mac_address, timestamp, device_name)
        VALUES (?, ?, ?, ?)
        ''', (ip_address, mac_address, timestamp, device_name))
        self.conn.commit()

    def get_device_history(self, identifier):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT * FROM device_history
        WHERE ip_address = ? OR mac_address = ?
        ORDER BY timestamp DESC
        ''', (identifier, identifier))
        return cursor.fetchall()

    def print_device_history(self, identifier):
        history = self.get_device_history(identifier)
        if not history:
            print(f"No history found for {identifier}")
            return

        print(f"History for {identifier}:")
        for entry in history:
            print(f"IP: {entry[1]}, MAC: {entry[2]}, Time: {entry[3]}, Device Name: {entry[4]}")

    def close(self):
        self.conn.close()

# Usage example
if __name__ == "__main__":
    tracker = NetworkHistoryTracker()
    
    # Capture ARP cache
    tracker.capture_arp_cache()
    
    # Print history for a specific IP or MAC address
    tracker.print_device_history('192.168.0.20')
    
    tracker.close()
