#===============================================================================
# MechaMule!
# Name(s):  Johnson Le
# Date: March 31, 2019
# File: Mule.py
# Desc: Hold settings for the mule. No handling.
#===============================================================================
# IMPORTS
#===============================================================================
import Echo
import Signal
import threading
import time
from RF24 import *
from MuleMotor_Functions import MOTOR
import RPi.GPIO as IO

class MULE(object):
    """Holds pins and setings for Mule.
    Parameters:
    (1) killswitch : Thread event to close all threads
    (2) pin_MTRS   : Array holding motor pins. enL, enR, dirL, dirR
    (3) pin_trig   : Int. Trigger pin
    (4) pin_ECHOS  : Array. Holds all echo pins. Ideally from left to right
    """
    def __init__(self, killswitch, pin_MTRS, pin_trig, pin_ECHOS, pin_nrf_int = 21, \
                 trig_hi=20E-6, trig_lo=120E-3, nrf_address=0xABCDEF):
        #store pins. might make them enum arrays.
        self.killswitch = killswitch
        self.pin_MTRS = pin_MTRS
        self.pin_trig = pin_trig
        self.pin_ECHOS = pin_ECHOS
        self.pin_nrf_int = pin_nrf_int
        self.echo = []
        self.nrf_address = nrf_address

        #main settings for
        self.trig_hi = trig_hi
        self.trig_lo = trig_lo

        #ping stuff. need to start trigger. echo works right away.
##        self.transmit = Signal.Generator(self.killswitch, self.pin_trig, self.trig_hi, self.trig_lo)
##        self.transmit.start()
        self.transmit = Signal.Pulser(self.killswitch, self.pin_trig, self.trig_hi, self.trig_lo)
        for i in range(0, len(self.pin_ECHOS)):
            self.echo.append(Echo.ECHO(self.pin_ECHOS[i]))

        #motor
        self.MTR = MOTOR(self.pin_MTRS[0], self.pin_MTRS[1], self.pin_MTRS[2], self.pin_MTRS[3])

        #nrf
        self.nrf = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)
        self.nrf.begin()
        self.nrf.enableDynamicPayloads()
        self.nrf.setRetries(15,15)
        self.nrf.openReadingPipe(1, self.nrf_address)
        self.nrf.startListening()

        IO.setwarnings(False)
        IO.setmode(IO.BCM)
        IO.setup(self.pin_nrf_int, IO.IN, pull_up_down=IO.PUD_UP)
        IO.add_event_detect(self.pin_nrf_int, IO.FALLING, callback=self.nrf_cb)
        

    def nrf_cb(self, channel):
        """callback function for nrf interrupt"""
        self.transmit.Pulse(1)
        self.nrf.read(self.nrf.getDynamicPayloadSize())
##        print("message: ", self.nrf.read(self.nrf.getDynamicPayloadSize()))

    def clean(self):
        """Cleans up the echo and motor pins"""
        print("Initiating mule cleansing.")
        for i in range(0, len(self.pin_ECHOS)):
            self.echo[i].clean()
        self.MTR.clean()
        IO.cleanup((21))


if __name__ == '__main__':
    print("Mule says hi")
    try:
        killswitch = threading.Event()
        mule = MULE(killswitch, [13,6,26,19], 17, [23,20], 21, 20E-6, 0)
        mule.MTR.Halt()
##        mule.MTR.Motor_L(-50)
##        mule.MTR.Motor_R(-50)
        while True:
            time.sleep(0.5)
            print("LEFT: ",2*mule.echo[0].GetInch()," <||> RIGHT: ", 2*mule.echo[1].GetInch())

    except KeyboardInterrupt:
        print("pressed ctrl+c")
    finally:
        print("goodbye")
        mule.MTR.Halt()
        killswitch.set()
        mule.clean()
        time.sleep(0.5)
