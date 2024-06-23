#!/usr/bin/env python3
import nmap
import subprocess
import ipaddress
import socket
import threading
from queue import Queue

# Function to check if nmap is installed
def check_nmap_installed():
    try:
        subprocess.run(["nmap", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

if not check_nmap_installed():
    print("Error: nmap is not installed. Please install nmap using 'sudo apt-get install nmap'")
    exit(1)

print(r"""______            _     _  ______                 _           _ 
                      #                   
 mmmm    mmm    mmm   #   m   mmm   m   m 
 #   #  #   #   #  #  #  m   #   m   m  m
 #   #  #####  #####  #*#    m####   #m#  
 ##m#"  "#mm"  "#mm"  #  "m  "mm"#   "#   
 #                                   m"   
 "                                  ''   """)
print("\n****************************************************************")
print("\n* Copyright of Perminus K., 2024                              *")
print("\n****************************************************************")

# Function to get the local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

# Function to get the hostname using reverse DNS lookup
def get_hostname(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.gaierror):
        return "Unknown"

# Get the local IP and calculate the network range
local_ip = get_local_ip()
network = ipaddress.IPv4Network(local_ip + '/24', strict=False)
start_ip = network.network_address
end_ip = network.broadcast_address

print(f"Scanning the network {network}")

# Thread worker function to scan an IP address
def scan_ip(q):
    nm = nmap.PortScanner()
    while not q.empty():
        ip_int = q.get()
        ip_str = str(ipaddress.IPv4Address(ip_int))
        try:
            result = nm.scan(ip_str, arguments='-sn')  # '-sn' for ping scan (no port scan)
            if 'up' in result['scan'][ip_str]['status']['state']:
                hostname = result['scan'][ip_str]['hostnames'][0]['name'] if result['scan'][ip_str]['hostnames'] else ''
                if not hostname:
                    hostname = get_hostname(ip_str)
                print(f"IP address {ip_str} is up. Hostname: {hostname}")
            else:
                print(f"IP address {ip_str} is down")
        except Exception as e:
            print(f"Cannot scan IP address {ip_str}. Error: {e}")
        q.task_done()

# Create a queue and add IP addresses to it
q = Queue()
for ip_int in range(int(start_ip), int(end_ip) + 1):
    q.put(ip_int)

# Create and start threads
num_threads = 50
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=scan_ip, args=(q,))
    t.start()
    threads.append(t)

# Wait for all threads to complete
for t in threads:
    t.join()

print("Scanning complete.")

