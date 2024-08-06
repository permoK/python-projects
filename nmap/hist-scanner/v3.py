import subprocess
import sqlite3
from datetime import datetime
import threading

def capture_packets():
    conn = sqlite3.connect('network_log.db')
    c = conn.cursor()

    capture_command = [
        'tshark', '-i', 'eth0', '-T', 'fields', '-e', 'frame.time', '-e', 'ip.src', '-e', 'ip.dst'
    ]

    proc = subprocess.Popen(capture_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    for line in proc.stdout:
        fields = line.strip().split('\t')
        if len(fields) == 3:
            timestamp = datetime.strptime(fields[0], "%b %d, %Y %H:%M:%S.%f %Z")
            src_ip = fields[1]
            dst_ip = fields[2]
            c.execute("INSERT INTO packets (timestamp, src_ip, dst_ip) VALUES (?, ?, ?)", (timestamp, src_ip, dst_ip))
            conn.commit()

    conn.close()

def get_ip_history(ip_address):
    conn = sqlite3.connect('network_log.db')
    c = conn.cursor()
    c.execute("SELECT * FROM packets WHERE src_ip=? OR dst_ip=?", (ip_address, ip_address))
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    capture_thread = threading.Thread(target=capture_packets)
    capture_thread.daemon = True
    capture_thread.start()

    while True:
        ip_address = input("Enter IP address to search: ")
        history = get_ip_history(ip_address)
        for entry in history:
            print(entry)

