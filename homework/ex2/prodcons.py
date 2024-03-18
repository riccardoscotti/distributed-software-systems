# Author: Riccardo Scotti (0001060133)
# Distributed Software Systems -- Prof. Paolo Ciancarini 
# Univeristà di Bologna -- A.Y. 2023/2024

import json
from queue import Queue 
import random
from threading import Thread, Lock 
import time 
from math import floor

# creation of lock
mutex = Lock()

# creation of shared buffer 
MAX_BUFF_SIZE = 10
buff = Queue(MAX_BUFF_SIZE)


class Producer:
    def __init__(self, id: int) -> None:
        self.id = id 

    def log(self, msg: str) -> None:
        print(f"\u001b[3{3 + self.id}m[Producer {self.id}] " + msg + "\033[0m")

    def __call__(self) -> None:
        for _ in range(MAX_BUFF_SIZE // 2):
            # creating random data
            value = {
                'x': floor(random.random() * 100),
                'y': floor(random.random() * 100)
            }

            self.log("Waiting on mutex.")
            mutex.acquire()
            self.log("Mutex acquired.")
            # critical section start

            # serializing data and inserting into buffer
            buff.put(json.dumps(value))
            self.log(f"Object {value} added to buffer.")

            # random amount of sleep to show concurrency 
            time.sleep(random.random())
            
            # self.log("Releasing mutex.")
            mutex.release()
            # critical section end

            

class Consumer:
    def __init__(self, id) -> None:
        self.id = id
    
    def log(self, msg: str) -> None:
        print(f"\033[0;3{self.id + 1}m[Consumer {self.id}] " + msg + "\033[0m")
    
    def __call__(self) -> None:
        for _ in range(MAX_BUFF_SIZE):
            self.log(f"Waiting on mutex.")
            mutex.acquire()
            self.log("Mutex acquired.")

            # critical section start 
            res = None

            # data are consumed only if buffer is not empty
            if(not buff.empty()):

                # consuming and deserializing data, them printing them
                res = json.loads(buff.get())
                self.log(f"Object ({res['x']}, {res['y']}) consumed from buffer.")
            else:
                self.log(f"No objects found in buffer.")

            # random amount of sleep to show concurrency
            time.sleep(random.random())
        
            # self.log("Releasing mutex.")
            mutex.release()
            # critical section end

if __name__ == "__main__":
    producer1 = Producer(1)
    producer2 = Producer(2)
    consumer = Consumer(1)
    
    
    prod1_thread = Thread(target=producer1)
    prod2_thread = Thread(target=producer2)
    cons_thread = Thread(target=consumer)

    print("[Main] Producer 1 thread start")
    prod1_thread.start()

    print("[Main] Producer 2 thread start")
    prod2_thread.start()

    print("[Main] Consumer thread start")
    cons_thread.start()