#!/usr/bin/env python3
import socket
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# Regular Expression Pattern to recognise IPv4 addresses.
ip_add_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
# Regular Expression Pattern to extract the number of ports you want to scan. 
# You have to specify <lowest_port_number>-<highest_port_number> (ex 10-100)
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")

# Initializing the port numbers
port_min = 0
port_max = 65535

# This function checks if a specific port is open on a given IP address
def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((ip, port))
            return port
    except:
        return None

# Ask user to input the IP address they want to scan.
while True:
    ip_add_entered = input("\nPlease enter the IP address that you want to scan: ")
    if ip_add_pattern.search(ip_add_entered):
        print(f"{ip_add_entered} is a valid IP address")
        break

while True:
    # You can scan 0-65535 ports. This scanner is basic and doesn't use multithreading so scanning all 
    # the ports is not advised.
    print("Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
    port_range = input("Enter port range: ")
    port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
    if port_range_valid:
        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        break

open_ports = []
# Use ThreadPoolExecutor to scan ports concurrently
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(is_port_open, ip_add_entered, port) for port in range(port_min, port_max + 1)]
    for future in as_completed(futures):
        port = future.result()
        if port:
            open_ports.append(port)

# We only care about the open ports.
for port in open_ports:
    print(f"Port {port} is open on {ip_add_entered}.")

