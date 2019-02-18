from pynput import keyboard
from queue import Queue
import time
import threading

class KB(threading.Thread):
    """Keyboard Thread
    Parameters:
    (1) stopper : threaded event for stopping threads
    (2) q : the queue to place the keyboard stuff too
    """
    def __init__(self, stopper, q):
        threading.Thread.__init__(self)
        self.q = q
        self.stopper = stopper
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        print(key)
        if key == keyboard.Key.esc:
            self.stopper.set()
        self.q.put(key.char)

    def run(self):
        self.listener.start()
        while (self.stopper.is_set() == False):
            pass
        self.listener.stop()
        print("Keyboard Thread Exit")



if __name__ == '__main__':
    def qworker(stopper):
        while (stopper.is_set() == False):
            print(q1.get())
            q1.task_done()
            
    q1 = Queue(maxsize=0)
    closer = threading.Event()
    for i in range(3):
        t = threading.Thread(target=qworker, kwargs=dict(stopper=closer))
        t.daemon = True
        t.start()

    kb = KB(closer, q1)
    kb.start()

    try:
        while (closer.is_set() == False):
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("closing program in .5 seconds")
        time.sleep(.5)
