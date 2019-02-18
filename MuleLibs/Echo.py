import RPi.GPIO as IO
import time
import math

class ECHO(object):
    """Don't forget to clean!!!!!!"""
    def __init__(self, pin, temp=20, IO_mode=IO.BCM):
        self.pin = pin
        self.temp = temp
        self.IO_mode = IO_mode
        
        self.t_start = 0
        self.t_end = 0
        self.TOF = 0
        self.cm = 0
        self.inch = 0
        self.meters = 0
        self.feet = 0
        self.state = IO.LOW

        self.speed_of_sound = 331.3 * math.sqrt(1+(self.temp / 273.15))

        IO.setwarnings(False)
        IO.setmode(self.IO_mode)
        IO.setup(self.pin, IO.IN, pull_up_down=IO.PUD_UP)

        IO.add_event_detect(self.pin, IO.BOTH, callback=self.callback)


    def callback(self, channel):
        if (IO.input(self.pin) == IO.HIGH):
            self.t_start = time.time()
        elif (IO.input(self.pin) == IO.LOW):
            self.t_end = time.time()
            self.TOF = self.t_end - self.t_start
            cm = self.TOF * ((self.speed_of_sound * 100)/2)
            self.cm = cm

    def clean(self):
        IO.cleanup((self.pin))

if __name__ == '__main__':
    p = 19
    yaaah = ECHO(p)
    

    try:
        while True:
            print(yaaah.cm*.393701)
            time.sleep(1)
    except KeyboardInterrupt:
        yaaah.clean()
        print("exit")
