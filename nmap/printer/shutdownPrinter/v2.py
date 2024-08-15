import socket

def send_pjl_shutdown(ip):
    pjl_command = b'\x1B%-12345X@PJL EOJ\r\n\x1B%-12345X'  # Example PJL command
    printer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    printer_socket.connect((ip, 9100))  # 9100 is the common port for PJL
    printer_socket.send(pjl_command)
    printer_socket.close()

# Replace '192.168.1.100' with your printer's IP address
send_pjl_shutdown('172.16.3.29')

