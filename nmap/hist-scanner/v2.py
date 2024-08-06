import subprocess
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('network_log.db')
c = conn.cursor()

# Packet capture setup
capture_command = [
    'tshark', '-i', 'eth0', '-T', 'fields', '-e', 'frame.time', '-e', 'ip.src', '-e', 'ip.dst'
]

proc = subprocess.Popen(capture_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Process captured packets
for line in proc.stdout:
    fields = line.strip().split('\t')
    if len(fields) == 3:
        timestamp = datetime.strptime(fields[0], "%b %d, %Y %H:%M:%S.%f %Z")
        src_ip = fields[1]
        dst_ip = fields[2]
        c.execute("INSERT INTO packets (timestamp, src_ip, dst_ip) VALUES (?, ?, ?)", (timestamp, src_ip, dst_ip))
        conn.commit()

conn.close()

