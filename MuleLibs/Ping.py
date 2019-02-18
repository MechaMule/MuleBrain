import time
import math
import RPi.GPIO as IO


class PING(object):
    """This is a class for interfacing a Ping Sensor.
    Object initialized with # parameters.
    Parameters:
    (1) pin_trig (int)  : default=None, help=pin trigger is connected to. None if not used.
    (2) pin_echo (int)  : default=None, help=pin echo is connected to. None if not used.
    (3) temp (int)      : default=20 celcius room temp, help=temperature affects speed of sound.
    (4) IO_mode (str)   : default=GPIO.BCM, help=GPIO.BCM or GPIO.BOARD.
    """
    def __init__(self, pin_trig, pin_echo, temp=20, IO_mode=IO.BCM):
        self.pin_trig = pin_trig
        self.pin_echo = pin_echo
        self.temp = temp
        self.IO_mode = IO_mode
        
        self.speed_of_sound = 331.3 * math.sqrt(1+(self.temp / 273.15))

    def raw_distance(self, sample_size=5, sample_delay=60e-3):
        """Returns raw distance value which can then be converted.
        Sample size determines how many runs to take and then averaging.
        Will be in meters.
        """
        sample = []
        IO.setwarnings(False)
        IO.setmode(self.IO_mode)
        IO.setup(self.pin_trig, IO.OUT)
        IO.setup(self.pin_echo, IO.IN)

        timeout = False

        for ewww in range(sample_size):
            # Pulse Trigger pin 10us
            IO.output(self.pin_trig, IO.LOW)
            time.sleep(sample_delay)
            IO.output(self.pin_trig, IO.HIGH)
            time.sleep(10e-6)
            IO.output(self.pin_trig, IO.LOW)

            # wait for echo to go high. will timeout if too long
            t1 = time.time()
            timeout = False
            while IO.input(self.pin_echo) == IO.LOW:
                if (time.time() - t1) > 30e-3:
                    timeout=True
                    break
                
            t_echostart = time.time()
            t1 = time.time()
            while IO.input(self.pin_echo) == IO.HIGH:
                if(time.time() - t1) > 0.034995626: #capping at 20feet
                    timeout=True

            if(timeout==False):
                t_echostop = time.time()
                t_flight = t_echostop - t_echostart
                cm = t_flight * ((self.speed_of_sound * 100)/2)
                sample.append(cm)
                
            elif(timeout==True):
                sample.append(0)

        IO.cleanup((self.pin_trig, self.pin_echo))

        new_sample = []
        for i in range(len(sample)):
            if sample[i] != 0:
                new_sample.append(sample[i])
        if len(new_sample) < 3:
            return 0
        
        sort = sorted(new_sample)
        return round(sort[len(sort) // 2], 3)

        
##        sort = sorted(sample)
##        num = sample_size
##        for i in range(len(sample)):
##            if sample[i] == 0:
##                num = num-1
##                
##        return round(sort[(sample_size // 2) + (num // 2)], 3)
        
##        avg = 0
##        num = sample_size
##        for i in range(len(sample)):
##            avg = avg + sample[i]
##            if(sample[i]==0):
##                num = num-1
##
##        if num == 0:
##            return 0
##        else:
##            return round(avg / num, 3)

if __name__ == "__main__":
    import MuleMotor_Functions as mtr
    
    trig = 13
    echo1 = 19
    echo2 = 26
    
    try:
        ping1 = PING(trig,echo1)
        ping2 = PING(trig,echo2)
        mtr.Motor_Init()
        while True:
            print("echo1: ", ping1.raw_distance(), "|| echo2: ", ping2.raw_distance())
##            diff = ping2.raw_distance() - ping1.raw_distance()
##            print(diff)
##            if(diff < 0):
##                mtr.RightMtrSpeed(-80)
##                mtr.LeftMtrSpeed(-30)
##            elif(diff > 0):
##                mtr.RightMtrSpeed(-30)
##                mtr.LeftMtrSpeed(-80)

        
    except KeyboardInterrupt:
        pass
    finally:
        IO.cleanup()

##            mtr.RightMtrSpeed(40)
##            mtr.LeftMtrSpeed(40)
  
