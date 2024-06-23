import socket
import pyautogui
import cv2
import numpy as np
import pickle

class RemoteAccessTool:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def start_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")
        
        while True:
            client, addr = self.socket.accept()
            print(f"Connection from {addr}")
            self.handle_client(client)

    def start_client(self):
        self.socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")
        
        while True:
            self.send_command()

    def handle_client(self, client):
        while True:
            data = client.recv(1024).decode()
            if not data:
                break
            
            if data.startswith("MOVE"):
                _, x, y = data.split()
                pyautogui.moveTo(int(x), int(y))
            elif data.startswith("CLICK"):
                pyautogui.click()
            elif data == "SCREENSHOT":
                self.send_screenshot(client)

        client.close()

    def send_command(self):
        command = input("Enter command (MOVE x y, CLICK, SCREENSHOT, or EXIT): ")
        if command.lower() == "exit":
            self.socket.close()
            return False
        self.socket.send(command.encode())
        
        if command == "SCREENSHOT":
            self.receive_screenshot()
        
        return True

    def send_screenshot(self, client):
        screenshot = pyautogui.screenshot()
        _, img_encoded = cv2.imencode('.png', np.array(screenshot))
        data = pickle.dumps(img_encoded)
        client.send(data)

    def receive_screenshot(self):
        data = b""
        while True:
            packet = self.socket.recv(4096)
            if not packet:
                break
            data += packet
        
        img_encoded = pickle.loads(data)
        screenshot = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
        cv2.imshow("Remote Screenshot", screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Usage
if __name__ == "__main__":
    host = "localhost"  # Replace with the actual IP address for remote connections
    port = 12345

    tool = RemoteAccessTool(host, port)

    mode = input("Enter 'server' or 'client': ")
    if mode.lower() == "server":
        tool.start_server()
    elif mode.lower() == "client":
        tool.start_client()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")
