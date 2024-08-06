import ipaddress
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from scapy.all import ARP, Ether, srp
import netifaces
import nmap

class EnhancedDeviceScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.network = self.get_local_network()

    def get_local_network(self):
        gateways = netifaces.gateways()
        default_interface = gateways['default'][netifaces.AF_INET][1]
        addrs = netifaces.ifaddresses(default_interface)[netifaces.AF_INET][0]
        return ipaddress.IPv4Network(f"{addrs['addr']}/{addrs['netmask']}", strict=False)

    def arp_scan(self, ip_range):
        arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
        return srp(arp_request, timeout=2, verbose=False)[0]

    def get_ip_mac_mapping(self):
        print("Performing initial ARP scan...")
        results = self.arp_scan(str(self.network))
        return {received.psrc: received.hwsrc for sent, received in results}

    def scan_device(self, ip, mac):
        try:
            self.nm.scan(ip, arguments='-O -sV -T4 --max-retries 1 --max-scan-delay 20ms')
            return {
                'ip': ip,
                'mac': mac,
                'hostname': self.nm[ip].hostname(),
                'os': self.nm[ip]['osmatch'][0]['name'] if 'osmatch' in self.nm[ip] and self.nm[ip]['osmatch'] else 'Unknown',
                'device_type': self.nm[ip]['osmatch'][0]['osclass'][0]['type'] if 'osmatch' in self.nm[ip] and self.nm[ip]['osmatch'] and 'osclass' in self.nm[ip]['osmatch'][0] else 'Unknown',
                'open_ports': list(self.nm[ip]['tcp'].keys()) if 'tcp' in self.nm[ip] else []
            }
        except Exception as e:
            print(f"Error scanning {ip}: {str(e)}")
            return None

    def filter_and_scan(self, filter_type, filter_value):
        ip_mac_mapping = self.get_ip_mac_mapping()
        
        if filter_type == 'mac':
            ip = next((ip for ip, mac in ip_mac_mapping.items() if mac.lower() == filter_value.lower()), None)
            if ip:
                return self.scan_device(ip, filter_value)
        elif filter_type == 'ip':
            if filter_value in ip_mac_mapping:
                return self.scan_device(filter_value, ip_mac_mapping[filter_value])
        
        print(f"No device found with the given {filter_type.upper()} address.")
        return None

def main():
    scanner = EnhancedDeviceScanner()
    
    while True:
        print("\nEnhanced Device Scanner")
        print("1. Scan by MAC address")
        print("2. Scan by IP address")
        print("3. Quit")
        
        choice = input("Select an option (1/2/3): ")
        
        if choice == '1':
            address = input("Enter the MAC address to scan: ")
            filter_type = 'mac'
        elif choice == '2':
            address = input("Enter the IP address to scan: ")
            filter_type = 'ip'
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue
        
        print(f"\nInitiating scan for {filter_type.upper()} address: {address}")
        start_time = time.time()
        
        result = scanner.filter_and_scan(filter_type, address)
        
        print(f"\nScan completed in {time.time() - start_time:.2f} seconds")
        
        if result:
            print("\nDevice Information:")
            print(f"IP Address: {result['ip']}")
            print(f"MAC Address: {result['mac']}")
            print(f"Hostname: {result['hostname']}")
            print(f"Operating System: {result['os']}")
            print(f"Device Type: {result['device_type']}")
            print(f"Open Ports: {', '.join(map(str, result['open_ports']))}")
        else:
            print("No information found for the given address.")

if __name__ == "__main__":
    main()
