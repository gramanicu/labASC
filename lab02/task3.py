'''
Coffee Factory: A multiple producer - multiple consumer approach

Generate a base class Coffee which knows only the coffee name
Create the Espresso, Americano and Cappuccino classes which inherit the base class knowing that
each coffee type has a predetermined size.
Each of these classes have a get message method

Create 3 additional classes as following:
    * Distributor - A shared space where the producers puts coffees and the consumers takes them
    * CoffeeFactory - An infinite loop, which always sends coffees to the distributor
    * User - Another infinite loop, which always takes coffees from the distributor

The scope of this exercise is to correctly use threads, classes and synchronization objects.
The size of the coffee (ex. small, medium, large) is chosen randomly everytime.
The coffee type is chosen randomly everytime.

Example of output:

Consumer 65 consumed espresso
Factory 7 produced a nice small espresso
Consumer 87 consumed cappuccino
Factory 9 produced an italian medium cappuccino
Consumer 90 consumed americano
Consumer 84 consumed espresso
Factory 8 produced a strong medium americano
Consumer 135 consumed cappuccino
Consumer 94 consumed americano
'''

from threading import Lock, Semaphore, Thread
from random import randint, seed
from time import sleep

# How many times will the producers/consumers loop
thread_loops = 3

class Coffee:
    # Base class
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_name(self):
        # Returns the coffee name
        return self.name

    def get_size(self):
        # Returns the coffee size
        return self.size

    def get_message(self):
        # Output message
        return "a " + self.size + " " + self.name

class Espresso(Coffee):
    # Espresso implementation
    def __init__(self, size):
        Coffee.__init__(self, 'espresso', size)  

    def get_message(self):
        # Output message
        return "a nice " + self.size + " " + self.name

class Americano(Coffee):
    # Americano implementation
    def __init__(self, size):
        Coffee.__init__(self, 'americano', size)  

    def get_message(self):
        # Output message
        return "a strong " + self.size + " " + self.name


class Cappuccino(Coffee):
    # Cappuccino implementation
    def __init__(self, size):
        Coffee.__init__(self, 'cappuccino', size)  

    def get_message(self):
        # Output message
        return "a italian " + self.size + " " + self.name

coffee_types = [Espresso, Americano, Cappuccino]
coffee_sizes = ['small', 'medium', 'large']

# The buffer from the producer-consumer problem
class Distributor():
    # Base class
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = []
        self.mutex = Lock()
        self.isfull = Semaphore(capacity) # Locks when full (Remaining capacity)
        self.isempty = Semaphore(0)  # Locks when empty (Used capacity)

    def produce(self, coffee):
        # If not full, continue
        self.isfull.acquire()
        
        # Place in buffer
        self.mutex.acquire()
        self.queue.append(coffee)
        self.mutex.release()

        # Use another space
        self.isempty.release()

    def consume(self):
        # If not empty, continue
        self.isempty.acquire()

        # Remove from buffer
        self.mutex.acquire()
        coffee = self.queue.pop(0)
        self.mutex.release()

        # Clear a space
        self.isfull.release()

        # Give the coffee to the consumer
        return coffee

# The producer from the producer-consumer problem
class CoffeeFactory(Thread):
    # Constructor
    def __init__(self, distributor, id):
        Thread.__init__(self)
        self.distributor = distributor
        self.id = id
    
    def run(self):
        added = 0
        while added != thread_loops:
            # Create a random coffee
            type = randint(0, len(coffee_types) - 1)
            size = randint(0, len(coffee_sizes) - 1)

            coffee = coffee_types[type](coffee_sizes[size])

            # Distribute the coffee
            self.distributor.produce(coffee)
            print("Producer", self.id, "added" , coffee.get_message())

            added = added + 1

            # Delay before the next one
            sleep(randint(5, 15)/ 10.0)
            

# The consumer from the producer-consumer problem
class User(Thread):
    # Constructor
    def __init__(self, distributor, id):
        Thread.__init__(self)
        self.distributor = distributor
        self.id = id
    
    def run(self):
        took = thread_loops
        while took != 0:
            # Get a coffee
            coffee = self.distributor.consume()
            print("Consumer", self.id, "took" , coffee.get_message())

            took = took - 1

            # Delay before the next one
            sleep(randint(5, 15) / 10.0)
            

if __name__ == '__main__':
    seed()

    # Initialise the buffer
    capacity = int(input("What is the distributor capacity? "))
    distributor = Distributor(capacity)

     # The list of threads
    consumers = []
    producers = []

    num_of_prods = int(input("How many producers? "))
    num_of_cons = int(input("How many consumers? "))

    cid = 0
    pid = 0

    # Create and start the producers
    for i in range(num_of_prods):
        t = CoffeeFactory(distributor, pid)
        pid = pid + 1
        producers.append(t)
        producers[i].start()

    # Create and start the consumers
    for i in range(num_of_cons):
        t = User(distributor, cid)
        cid = cid + 1
        consumers.append(t)
        consumers[i].start()

    # Wait for the threads to finish
    for i in range(len(producers)):
        producers[i].join()
    for i in range(len(consumers)):
        consumers[i].join()
