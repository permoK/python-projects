import ipaddress
import socket
import threading
import queue
import time
from scapy.all import ARP, Ether, srp
import netifaces
import nmap
import csv

class NetworkScanner:
    def __init__(self):
        self.ip_queue = queue.Queue()
        self.result_dict = {}
        self.lock = threading.Lock()

    def get_local_ip_and_network(self):
        gateways = netifaces.gateways()
        default_gateway = gateways['default'][netifaces.AF_INET][0]
        default_interface = gateways['default'][netifaces.AF_INET][1]
        addrs = netifaces.ifaddresses(default_interface)
        ip_info = addrs[netifaces.AF_INET][0]
        address = ip_info['addr']
        netmask = ip_info['netmask']
        cidr = ipaddress.IPv4Network(f"{address}/{netmask}", strict=False)
        return str(cidr)

    def get_mac_address(self, ip):
        try:
            arp_request = ARP(pdst=ip)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp_request
            result = srp(packet, timeout=3, verbose=False)[0]
            return result[0][1].hwsrc
        except:
            return None

    def worker(self):
        nm = nmap.PortScanner()
        while True:
            try:
                ip = self.ip_queue.get_nowait()
                mac = self.get_mac_address(ip)
                if mac:
                    nm.scan(ip, arguments='-O -sV')
                    with self.lock:
                        self.result_dict[ip] = {
                            'mac': mac,
                            'hostname': nm[ip].hostname() if 'hostname' in nm[ip] else '',
                            'os': nm[ip]['osmatch'][0]['name'] if 'osmatch' in nm[ip] and nm[ip]['osmatch'] else 'Unknown',
                            'device_type': nm[ip]['osmatch'][0]['osclass'][0]['type'] if 'osmatch' in nm[ip] and nm[ip]['osmatch'] and 'osclass' in nm[ip]['osmatch'][0] else 'Unknown'
                        }
                self.ip_queue.task_done()
            except queue.Empty:
                break

    def scan_network(self, num_threads=20):
        network = self.get_local_ip_and_network()
        print(f"Detected network: {network}")
        
        for ip in ipaddress.IPv4Network(network):
            self.ip_queue.put(str(ip))

        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        return self.result_dict

def main():
    scanner = NetworkScanner()
    print("Initializing network scan...")
    start_time = time.time()
    results = scanner.scan_network()
    print(f"\nScan completed in {time.time() - start_time:.2f} seconds")
    print(f"Found {len(results)} devices:")
    
    # Save results to CSV file
    csv_filename = 'network_scan_results.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'MAC', 'Hostname', 'OS', 'Device Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for ip, info in results.items():
            writer.writerow({
                'IP': ip,
                'MAC': info['mac'],
                'Hostname': info['hostname'],
                'OS': info['os'],
                'Device Type': info['device_type']
            })
    
    print(f"\nResults saved to {csv_filename}")
    
    # Print results to console
    for ip, info in results.items():
        print(f"IP: {ip}")
        print(f"  MAC: {info['mac']}")
        print(f"  Hostname: {info['hostname']}")
        print(f"  OS: {info['os']}")
        print(f"  Device Type: {info['device_type']}")
        print()

if __name__ == "__main__":
    main()
