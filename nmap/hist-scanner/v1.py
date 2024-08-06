import sqlite3
from scapy.all import *
import datetime

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

    def capture_network_traffic(self, interface='eth0', duration=60):
        packets = sniff(iface=interface, timeout=duration)
        for packet in packets:
            if IP in packet and Ether in packet:
                ip_address = packet[IP].src
                mac_address = packet[Ether].src
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
    
    # Capture network traffic for 5 minutes
    tracker.capture_network_traffic(duration=300)
    
    # Print history for a specific IP or MAC address
    tracker.print_device_history('192.168.1.100')
    
    tracker.close()
