import threading


lock = threading.Lock()

def synchronized_print(lock, message):
    with lock:
        print(message)

t1 = threading.Thread(target=synchronized_print, args=(lock, "Thread 1"))
t2 = threading.Thread(target=synchronized_print, args=(lock, "Thread 2"))
t1.start()
t2.start()
t1.join()
t2.join()

