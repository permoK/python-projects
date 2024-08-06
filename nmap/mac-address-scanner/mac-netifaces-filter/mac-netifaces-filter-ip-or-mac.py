import ipaddress
import socket
import threading
import queue
import time
from scapy.all import ARP, Ether, srp
import netifaces
import nmap

class DeviceScanner:
    def __init__(self):
        self.result = {}
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

    def get_ip_from_mac(self, mac_address):
        network = self.get_local_ip_and_network()
        arp_request = ARP(pdst=network)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp_request
        result = srp(packet, timeout=3, verbose=False)[0]
        
        for sent, received in result:
            if received.hwsrc.lower() == mac_address.lower():
                return received.psrc
        return None

    def get_mac_from_ip(self, ip_address):
        arp_request = ARP(pdst=ip_address)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp_request
        result = srp(packet, timeout=3, verbose=False)[0]
        
        if result:
            return result[0][1].hwsrc
        return None

    def scan_device(self, address, address_type):
        if address_type == 'mac':
            ip = self.get_ip_from_mac(address)
            mac = address
        else:  # address_type == 'ip'
            ip = address
            mac = self.get_mac_from_ip(ip)

        if not ip or not mac:
            print(f"Could not find {'IP' if address_type == 'mac' else 'MAC'} for given {address_type.upper()} address: {address}")
            return None

        nm = nmap.PortScanner()
        nm.scan(ip, arguments='-O -sV')

        with self.lock:
            self.result = {
                'ip': ip,
                'mac': mac,
                'hostname': nm[ip].hostname() if 'hostname' in nm[ip] else '',
                'os': nm[ip]['osmatch'][0]['name'] if 'osmatch' in nm[ip] and nm[ip]['osmatch'] else 'Unknown',
                'device_type': nm[ip]['osmatch'][0]['osclass'][0]['type'] if 'osmatch' in nm[ip] and nm[ip]['osmatch'] and 'osclass' in nm[ip]['osmatch'][0] else 'Unknown',
                'open_ports': list(nm[ip]['tcp'].keys()) if 'tcp' in nm[ip] else []
            }

        return self.result

def main():
    scanner = DeviceScanner()
    
    while True:
        print("\nChoose an option:")
        print("1. Scan by MAC address")
        print("2. Scan by IP address")
        print("3. Quit")
        
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            address = input("Enter the MAC address to scan: ")
            address_type = 'mac'
        elif choice == '2':
            address = input("Enter the IP address to scan: ")
            address_type = 'ip'
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue
        
        print(f"\nScanning for {address_type.upper()} address: {address}")
        start_time = time.time()
        
        result = scanner.scan_device(address, address_type)
        
        print(f"\nScan completed in {time.time() - start_time:.2f} seconds")
        
        if result:
            print("Device information:")
            print(f"IP: {result['ip']}")
            print(f"MAC: {result['mac']}")
            print(f"Hostname: {result['hostname']}")
            print(f"OS: {result['os']}")
            print(f"Device Type: {result['device_type']}")
            print(f"Open Ports: {', '.join(map(str, result['open_ports']))}")
        else:
            print("No information found for the given address.")

if __name__ == "__main__":
    main()
