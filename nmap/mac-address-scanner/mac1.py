import socket
import struct
import threading
import queue
import time
from scapy.all import ARP, Ether, srp
import csv

def get_mac_address(ip):
    try:
        arp_request = ARP(pdst=ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp_request
        result = srp(packet, timeout=3, verbose=False)[0]
        return result[0][1].hwsrc
    except:
        return None

def worker(ip_queue, result_dict):
    while True:
        try:
            ip = ip_queue.get_nowait()
            mac = get_mac_address(ip)
            if mac:
                result_dict[ip] = mac
            ip_queue.task_done()
        except queue.Empty:
            break

def scan_network(ip_range, num_threads=20):
    ip_queue = queue.Queue()
    result_dict = {}

    # Populate the queue with IP addresses
    for ip in ip_range:
        ip_queue.put(ip)

    # Create and start worker threads
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(ip_queue, result_dict))
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    return result_dict

def main():
    start_ip = "15.15.21.0"  # Replace with your network's start IP
    end_ip = "15.15.21.254"  # Replace with your network's end IP

    # Generate IP range
    start = struct.unpack('>I', socket.inet_aton(start_ip))[0]
    end = struct.unpack('>I', socket.inet_aton(end_ip))[0]
    ip_range = [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end + 1)]

    print(f"Scanning IP range from {start_ip} to {end_ip}")
    start_time = time.time()

    results = scan_network(ip_range)

    print(f"\nScan completed in {time.time() - start_time:.2f} seconds")
    print(f"Found {len(results)} devices:")
    for ip, mac in results.items():
        print(f"IP: {ip}\tMAC: {mac}")

    # save in a csv file 
    
    csv_filename = f'mac-scanner({start_ip}-{end_ip}).csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'MAC']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for ip, mac in results.items():
            writer.writerow({
                'IP': ip,
                'MAC': mac
                })
            
        print(f"\nResults saved to {csv_filename}")


if __name__ == "__main__":
    main()
