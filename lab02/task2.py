"""
    Basic thread handling exercise:

    Use the Thread class to create and run more than 10 threads which print their name and a random
    number they receive as argument. The number of threads must be received from the command line.

    e.g. Hello, I'm Thread-96 and I received the number 42

"""
from random import randint, seed
from threading import Semaphore, Thread
import threading

# Thread Class
class SimpleThread(Thread):
    # Constructor
    def __init__(self, nr):
        Thread.__init__(self)
        self.nr = nr
 
    # Main Thread Code
    def run(self):
        print ("Hello, I'm Thread-", threading.get_ident(), "and I received the number", self.nr)

# The list of threads
thread_list = []

# Initialise the rng
seed()
 
# pornim thread-urile
for i in range(10):
    thread = Thread(target = access, args = (i, semafor))
    thread.start()
    thread_list.append(thread)
 
# asteptam terminarea thread-urilor
for i in range(len(thread_list)):
    thread_list[i].join()
