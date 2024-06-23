#!/usr/bin/env python3
import nmap
import re
import subprocess
import ipaddress
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

# Regular Expression Pattern to recognise IPv4 addresses.
ip_add_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

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

while True:
    ip_range = input("\nPlease enter the range of IP addresses you want to scan (format: start_ip-end_ip): ")
    try:
        start_ip, end_ip = ip_range.split('-')
        if ip_add_pattern.search(start_ip) and ip_add_pattern.search(end_ip):
            start_ip = ipaddress.IPv4Address(start_ip)
            end_ip = ipaddress.IPv4Address(end_ip)
            if start_ip <= end_ip:
                print(f"Scanning from {start_ip} to {end_ip}")
                break
            else:
                print("Error: Start IP should be less than or equal to End IP")
        else:
            print("Error: Invalid IP address format")
    except ValueError:
        print("Error: Invalid input format. Please use format: start_ip-end_ip")

# Thread worker function to scan an IP address
def scan_ip(q):
    nm = nmap.PortScanner()
    while not q.empty():
        ip_int = q.get()
        ip_str = str(ipaddress.IPv4Address(ip_int))
        try:
            result = nm.scan(ip_str, arguments='-sn')  # '-sn' for ping scan (no port scan)
            if 'up' in result['scan'][ip_str]['status']['state']:
                hostname = result['scan'][ip_str]['hostnames'][0]['name'] if result['scan'][ip_str]['hostnames'] else 'Unknown'
                print(f"IP address {ip_str} is up. Hostname: {hostname}")
            else:
                print(f"IP address {ip_str} is down")
        except Exception as e:
            pass
            # print(f"Cannot scan IP address {ip_str}. Error: {e}")
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

