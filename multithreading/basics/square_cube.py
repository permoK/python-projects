import time
import threading


def square_num(arr):
    for i in arr:
        # sleep to delay the execution time
        time.sleep(0.2)
        print(f'square of {i}: {i*i}')

def cube_num(arr):
    # sleep to delay the execution time
    time.sleep(0.2)
    for i in arr:
        print(f'cube of {i}: {i*i*i}')

arr = [2,3,5]

t = time.time()

# without threading
# square_num(arr)
# cube_num(arr)


# With threading
t1 = threading.Thread(target=square_num, args=(arr,))
t2 = threading.Thread(target=cube_num, args=(arr,))

t1.start()
t2.start()

t1.join()
t2.join()

print(time.time()-t)
