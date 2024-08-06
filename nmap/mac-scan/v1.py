import threading
from queue import Queue
import subprocess
import re
import time

def ping(ip):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", ip], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def get_mac(ip):
    try:
        output = subprocess.check_output(["arp", "-n", ip]).decode("utf-8")
        mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", output, re.IGNORECASE)
        if mac:
            return mac.group(0)
    except subprocess.CalledProcessError:
        pass
    return None

def network_scanner(q, results):
    while True:
        ip = q.get()
        if ping(ip):
            mac = get_mac(ip)
            if mac:
                results.append((ip, mac))
        q.task_done()

def main():
    ip_range = "192.168.1."  # Adjust this to match your network
    num_threads = 100
    queue = Queue()
    results = []

    # Start worker threads
    for _ in range(num_threads):
        t = threading.Thread(target=network_scanner, args=(queue, results))
        t.daemon = True
        t.start()

    # Put IP addresses into the queue
    for i in range(1, 255):
        queue.put(f"{ip_range}{i}")

    # Wait for all tasks to complete
    queue.join()

    # Print results
    print("IP Address\t\tMAC Address")
    print("-" * 40)
    for ip, mac in sorted(results):
        print(f"{ip}\t\t{mac}")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nScan completed in {time.time() - start_time:.2f} seconds")
