import time
from threading import Thread
import multiprocessing


def synch_wait(kek):
    t_s = time.time()
    t_d = time.time()
    while t_d - t_s < kek:
        t_d = time.time()
        print(t_d - t_s)
    return 0

def tasktest():
    while True:
        print("Synch works")
    return 0
def main():
    t = Thread(target=synch_wait(15)).start()
    e = Thread(target=tasktest()).start()

if __name__ == "__main__":
    main()