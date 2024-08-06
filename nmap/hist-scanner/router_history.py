import requests
import re
from getpass import getpass
import csv
from datetime import datetime

class RouterHistoryViewer:
    def __init__(self, router_ip, username, password):
        self.router_ip = router_ip
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        login_url = f"http://{self.router_ip}/login.cgi"
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.session.post(login_url, data=payload)
        return response.status_code == 200

    def get_log(self):
        log_url = f"http://{self.router_ip}/log.htm"
        response = self.session.get(log_url)
        return response.text

    def parse_log(self, log_content):
        # This regex pattern might need to be adjusted based on your router's log format
        pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(http[s]?://\S+)"
        matches = re.findall(pattern, log_content, re.DOTALL)
        return matches

    def save_to_csv(self, data, filename="router_history.csv"):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "IP Address", "URL"])
            writer.writerows(data)

    def view_history(self):
        if self.login():
            log_content = self.get_log()
            parsed_data = self.parse_log(log_content)
            self.save_to_csv(parsed_data)
            print(f"Log saved to router_history.csv")
            return parsed_data
        else:
            print("Login failed. Please check your credentials.")
            return None

if __name__ == "__main__":
    router_ip = input("Enter your router's IP address: ")
    username = input("Enter your router's admin username: ")
    password = getpass("Enter your router's admin password: ")

    viewer = RouterHistoryViewer(router_ip, username, password)
    history = viewer.view_history()

    if history:
        print("\nRecent History:")
        for entry in history[:10]:  # Display the 10 most recent entries
            print(f"Time: {entry[0]}, IP: {entry[1]}, URL: {entry[2]}")
