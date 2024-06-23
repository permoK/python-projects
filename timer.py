import time

def timer(seconds):
    print(f"Timer started for {seconds} seconds.")
    while True:
        print(f"{seconds} seconds remaining.")
        time.sleep(seconds)
    
# if __name__ == "__main__":
#     seconds = int(input("Enter the number of seconds for the timer: "))
#     timer(seconds)

