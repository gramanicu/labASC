from threading import Barrier, Lock, Thread

''' 
Only one philosopher will eat at a time
I know this is actually pretty much removing the parallelism, but I can't
find a way to make all the threads act the same (as specified in the tasks
statement). If this limitation didn't exist, one efficient way would have
been to assign an id to each thread, and the ones with even id's would
"eat" first. Or, the simplest solution would be to make one thread "eat"
first, and this would remove the possibility for a deadlock.
'''

# Make true to actually make the program run in parallel
no_limit = False 

eating = Lock()

# When all the philosophers are hungry, they will try to eat
are_hungry = None

class Philosopher(Thread):
    def __init__(self, forks, l_fork, r_fork):
        Thread.__init__(self)

        # By convention, the right fork will have the same id
        self.__id = r_fork

        self.__forks = forks
        self.__l_fork = l_fork
        self.__r_fork = r_fork

    def run(self):
        # Wait for all the philosophers
        global are_hungry
        are_hungry.wait()

        if no_limit:
             # Half of the philosophers will eat first
            if self.__id % 2 == 0: 
                self.__forks[self.__l_fork].acquire()
                self.__forks[self.__r_fork].acquire()
                print("Philosopher", self.__id, "has eaten!")
                self.__forks[self.__r_fork].release()
                self.__forks[self.__l_fork].release()
            else:
                self.__forks[self.__r_fork].acquire()
                self.__forks[self.__l_fork].acquire()
                print("Philosopher", self.__id, "has eaten!")
                self.__forks[self.__l_fork].release()
                self.__forks[self.__r_fork].release()
        else:
            # Only one will eat at a time
            eating.acquire()
            self.__forks[self.__l_fork].acquire()
            self.__forks[self.__r_fork].acquire()
            print("A philosopher has eaten!")
            self.__forks[self.__l_fork].release()
            self.__forks[self.__r_fork].release()
            eating.release()

def main():
    forks = []
    philosophers = []

    p_num = int(input("How many philosophers? "))

    global are_hungry
    are_hungry = Barrier(p_num)

    # Initialise the locks (forks)
    for i in range(p_num):
        l = Lock()
        forks.append(l)

    # Initialise & start the threads (philosophers)
    for i in range(p_num):
        # Give each person a left and right fork
        t = Philosopher(forks, i - 1 if i > 0 else p_num - 1, i)
        philosophers.append(t)
        philosophers[i].start()

    # Wait for the threads to stop (philosophers stop eating)
    for i in range(p_num):
        philosophers[i].join()
    
    print("All philosophers have eaten!")


if __name__ == '__main__':
    main()