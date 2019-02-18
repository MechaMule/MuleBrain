from queue import Queue
import threading

class QueueThread(threading.Thread):
    def __init__(self, stopper, num_threads):
        threading.Thread.__init__(self)
        self.stopper = stopper
        self.num_threads = num_threads
        self.q = Queue(maxsize=0)

    def run(self):
        for i in range(self.num_threads):
            pass

#actually, don't think i need a module for queues. just make one in main

