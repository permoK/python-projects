import scapy.all as scapy
import time
import csv
from datetime import datetime
import threading
import ipaddress
import argparse
import logging

class NetworkMonitor:
    def __init__(self, network, interval=300, output_file='network_devices.csv'):
        self.network = network
        self.interval = interval
        self.output_file = output_file
        self.devices = {}
        self.lock = threading.Lock()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def scan_network(self):
        arp_request = scapy.ARP(pdst=self.network)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        
        devices = []
        for element in answered_list:
            device = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            devices.append(device)
        return devices

    def update_devices(self, devices):
        with self.lock:
            for device in devices:
                if device['mac'] not in self.devices:
                    self.devices[device['mac']] = {
                        'ip': device['ip'],
                        'first_seen': datetime.now(),
                        'last_seen': datetime.now()
                    }
                else:
                    self.devices[device['mac']]['last_seen'] = datetime.now()
                    if self.devices[device['mac']]['ip'] != device['ip']:
                        self.logger.info(f"IP change detected for {device['mac']}: {self.devices[device['mac']]['ip']} -> {device['ip']}")
                        self.devices[device['mac']]['ip'] = device['ip']

    def save_to_csv(self):
        with self.lock:
            with open(self.output_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['MAC', 'IP', 'First Seen', 'Last Seen'])
                for mac, data in self.devices.items():
                    writer.writerow([mac, data['ip'], data['first_seen'], data['last_seen']])
        self.logger.info(f"Data saved to {self.output_file}")

    def monitor(self):
        while True:
            try:
                devices = self.scan_network()
                self.update_devices(devices)
                self.save_to_csv()
                time.sleep(self.interval)
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                time.sleep(60)  # Wait a minute before retrying

    def start(self):
        self.logger.info(f"Starting network monitoring on {self.network}")
        monitor_thread = threading.Thread(target=self.monitor)
        monitor_thread.start()
        return monitor_thread

def parse_arguments():
    parser = argparse.ArgumentParser(description="Network Device Monitor")
    parser.add_argument("--network", required=True, help="Network to monitor (e.g., 192.168.1.0/24)")
    parser.add_argument("--interval", type=int, default=300, help="Scan interval in seconds (default: 300)")
    parser.add_argument("--output", default="network_devices.csv", help="Output CSV file (default: network_devices.csv)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    try:
        ipaddress.ip_network(args.network)
    except ValueError:
        print("Error: Invalid network format. Please use CIDR notation (e.g., 192.168.1.0/24)")
        exit(1)

    monitor = NetworkMonitor(args.network, args.interval, args.output)
    monitor_thread = monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the monitor...")
        monitor_thread.join()
        print("Monitor stopped.")
