import threading
from queue import Queue
import subprocess
import re
import time
import ipaddress

def ping(ip):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", str(ip)], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def get_mac(ip):
    try:
        output = subprocess.check_output(["arp", "-n", str(ip)]).decode("utf-8")
        mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", output, re.IGNORECASE)
        if mac:
            return mac.group(0)
    except subprocess.CalledProcessError:
        pass
    return None

def ip_scanner(q, active_ips):
    while True:
        ip = q.get()
        if ping(ip):
            active_ips.append(ip)
        q.task_done()

def mac_scanner(q, results):
    while True:
        ip = q.get()
        mac = get_mac(ip)
        if mac:
            results.append((str(ip), mac))
        q.task_done()

def main():
    network = "192.168.1.0/24"  # Adjust this to match your network
    num_threads = 100
    ip_queue = Queue()
    mac_queue = Queue()
    active_ips = []
    results = []

    # Start IP scanner threads
    for _ in range(num_threads):
        t = threading.Thread(target=ip_scanner, args=(ip_queue, active_ips))
        t.daemon = True
        t.start()

    # Put IP addresses into the queue
    for ip in ipaddress.IPv4Network(network):
        ip_queue.put(ip)

    # Wait for IP scanning to complete
    ip_queue.join()

    print(f"Found {len(active_ips)} active IP addresses")

    # Start MAC scanner threads
    for _ in range(num_threads):
        t = threading.Thread(target=mac_scanner, args=(mac_queue, results))
        t.daemon = True
        t.start()

    # Put active IPs into the MAC scanning queue
    for ip in active_ips:
        mac_queue.put(ip)

    # Wait for MAC scanning to complete
    mac_queue.join()

    # Print results
    print("\nIP Address\t\tMAC Address")
    print("-" * 40)
    for ip, mac in sorted(results):
        print(f"{ip}\t\t{mac}")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nScan completed in {time.time() - start_time:.2f} seconds")
