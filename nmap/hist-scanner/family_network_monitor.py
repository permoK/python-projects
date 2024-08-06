from scapy.all import ARP, Ether, srp, sniff, IP
import time
from datetime import datetime
import csv
import threading
import argparse
import logging
import ipaddress

class FamilyNetworkMonitor:
    def __init__(self, network, interval=300, output_file='family_network_activity.csv'):
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
        arp_request = ARP(pdst=self.network)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        
        devices = []
        for element in answered_list:
            device = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            devices.append(device)
        return devices

    def update_devices(self, devices):
        with self.lock:
            for device in devices:
                if device['ip'] not in self.devices:
                    self.devices[device['ip']] = {
                        'mac': device['mac'],
                        'first_seen': datetime.now(),
                        'last_seen': datetime.now(),
                        'total_traffic': 0,
                        'dns_queries': set()
                    }
                else:
                    self.devices[device['ip']]['last_seen'] = datetime.now()

    def packet_callback(self, packet):
        if IP in packet:
            src_ip = packet[IP].src
            if src_ip in self.devices:
                with self.lock:
                    self.devices[src_ip]['total_traffic'] += len(packet)
                    if packet.haslayer('DNS') and packet['DNS'].qr == 0:  # DNS query
                        self.devices[src_ip]['dns_queries'].add(packet['DNS'].qd.qname.decode())

    def monitor_traffic(self):
        sniff(prn=self.packet_callback, store=0, filter="ip")

    def save_to_csv(self):
        with self.lock:
            with open(self.output_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['IP', 'MAC', 'First Seen', 'Last Seen', 'Total Traffic (bytes)', 'Top DNS Queries'])
                for ip, data in self.devices.items():
                    top_dns = '; '.join(list(data['dns_queries'])[:5])  # Top 5 DNS queries
                    writer.writerow([ip, data['mac'], data['first_seen'], data['last_seen'], 
                                     data['total_traffic'], top_dns])
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
        self.logger.info(f"Starting family network monitoring on {self.network}")
        monitor_thread = threading.Thread(target=self.monitor)
        monitor_thread.start()
        traffic_thread = threading.Thread(target=self.monitor_traffic)
        traffic_thread.start()
        return monitor_thread, traffic_thread

def parse_arguments():
    parser = argparse.ArgumentParser(description="Family Network Activity Monitor")
    parser.add_argument("--network", required=True, help="Network to monitor (e.g., 192.168.1.0/24)")
    parser.add_argument("--interval", type=int, default=300, help="Scan interval in seconds (default: 300)")
    parser.add_argument("--output", default="family_network_activity.csv", help="Output CSV file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    try:
        ipaddress.ip_network(args.network)
    except ValueError:
        print("Error: Invalid network format. Please use CIDR notation (e.g., 192.168.1.0/24)")
        exit(1)

    monitor = FamilyNetworkMonitor(args.network, args.interval, args.output)
    monitor_thread, traffic_thread = monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the monitor...")
        monitor_thread.join()
        print("Monitor stopped.")
