#!/usr/bin/env python3
import nmap
import re
import subprocess
import ipaddress

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

nm = nmap.PortScanner()
for ip_int in range(int(start_ip), int(end_ip) + 1):
    ip_str = str(ipaddress.IPv4Address(ip_int))
    try:
        result = nm.scan(ip_str, '1')  # Scanning port 1 as a placeholder to check if the host is up
        if 'up' in result['scan'][ip_str]['status']['state']:
            print(f"IP address {ip_str} is up")
        else:
            print(f"IP address {ip_str} is down")
    except Exception as e:
        pass
        # print(f"Cannot scan IP address {ip_str}. Error: {e}")

