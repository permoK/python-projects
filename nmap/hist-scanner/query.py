import sqlite3

def get_ip_history(ip_address):
    conn = sqlite3.connect('network_log.db')
    c = conn.cursor()
    c.execute("SELECT * FROM packets WHERE src_ip=? OR dst_ip=?", (ip_address, ip_address))
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    ip_address = input("Enter IP address to search: ")
    history = get_ip_history(ip_address)
    for entry in history:
        print(entry)

