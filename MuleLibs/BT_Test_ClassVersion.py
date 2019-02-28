from bluedot.btcomm import BluetoothServer
import Signal
from queue import Queue
import time
import RPi.GPIO as GPIO

LED_W = 17
LED_B = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_W, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_B, GPIO.OUT, initial=GPIO.LOW)

class SendMsg:
    def __init__(self, q, LED_Y=25, LED_G=27, saved_msg="NO_MESSAGE", GPIO_mode=GPIO.BCM):
        self.q = q
        self.LED_Y = LED_Y
        self.LED_G = LED_G
        self.saved_msg = saved_msg
        self.Server = BluetoothServer(self.data_received)
        self.GPIO_mode = GPIO_mode
        GPIO.setwarnings(False)
        GPIO.setmode(self.GPIO_mode)
        if self.LED_Y == 0 and self.LED_G == 0:
            pass
        else:
            GPIO.setup(self.LED_Y, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.LED_G, GPIO.OUT, initial=GPIO.LOW)

    def retrieve_data(self):
        #print("Received", data)
        return self.saved_msg
#    def Get_Msg(self, getMsg):
#        return self.getMsg

    def setHighLow_Y(self, Flag):
        if(GPIO.input(self.LED_Y) and Flag is False):
            GPIO.output(self.LED_Y, GPIO.LOW)
        elif (not GPIO.input(self.LED_Y) and Flag is True):
            print("Turning on Yellow Button Led")
            GPIO.output(self.LED_Y, GPIO.HIGH)
        else:
            pass

    def setHighLow_G(self, Flag):
        if(GPIO.input(self.LED_G) and Flag is False):
            GPIO.output(self.LED_G, GPIO.LOW)
        elif (not GPIO.input(self.LED_G) and Flag is True):
            print("Turning on Green Button Led")
            GPIO.output(self.LED_G, GPIO.HIGH)


    def ClearSaved_Msg(self):
        self.saved_msg = "CLEARED_MESSAGE"
        return self.saved_msg

    def data_received(self, data):
        print("Received", data)
        self.q.put(data)
        self.saved_msg = data



#save_msg = "Nothing meaningful"
#Server = BluetoothServer(data_received)

if __name__ == "__main__":
    Led1 = 25
    Led2 = 27
    Msg1 = SendMsg(Led1, Led2)
    Flag_Y = True
    Flag_G = True
    try:
        print("=================Starting test=====================")

        while True:
            BT_Msg = Msg1.retrieve_data()
            #print(BT_Msg)
            #print('Saved string: {}'.format(Save_Str))
            if BT_Msg == 'DIST_5FT':
                print("Distance is now set to: 5FT")
                Flag_G = True
                Msg1.setHighLow_G(Flag_G)
                Msg1.ClearSaved_Msg()
<<<<<<< HEAD
            
            elif BT_Msg == 'DIST_10FT':
                print("Distance is now set to: 10FT")
=======

            elif BT_Msg == 'GP17_LIT':
                print("Going to Calibration settings")
>>>>>>> 1b9377d38308190d185f2296fbe696946bd521d4
                Flag_Y = True
                Msg1.setHighLow_Y(Flag_Y)
                Msg1.ClearSaved_Msg()

            elif BT_Msg == 'DIST_15FT':
                print("Distance is now set to: 15FT")
                GPIO.output(LED_W, GPIO.HIGH)
                Msg1.ClearSaved_Msg()


            elif BT_Msg == 'STOP':
                print("The bot will now stop")
                GPIO.output(LED_B, GPIO.HIGH)
                Msg1.ClearSaved_Msg()
            
            else:
                Msg1.setHighLow_Y(not Flag_Y)
                Msg1.setHighLow_G(not Flag_G)
                GPIO.output(LED_W, GPIO.LOW)
                GPIO.output(LED_B, GPIO.LOW)
            print (BT_Msg)
            time.sleep(1/2)
    except KeyboardInterrupt:
        print("Exiting program via CTRL + C")

    finally:
        GPIO.cleanup()
