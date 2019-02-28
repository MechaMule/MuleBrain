from bluedot.btcomm import BluetoothClient 
import time
import RPi.GPIO as GPIO

#================== Pre-defined messages ================
Pressed_G = "GP27_LIT"
Pressed_Y = "GP17_LIT"  # will make it activate comands later
#========================================================

BUTTON_G = 27
BUTTON_Y = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_G, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_Y, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

received = False



def data_received(data):
    print("received: ", data)
    c.send(data)
    global received
    received = True
    


if __name__ == "__main__":

    PiZero_Client = BluetoothClient("johnpi", data_received)

    try:
        print("============= Starting bluetooth button activation test ============")
        

        while True:
            
            if GPIO.input(BUTTON_G) == GPIO.HIGH:
                PiZero_Client.send(Pressed_G)
                print('Green button was pressed, should send message')
            elif GPIO.input(BUTTON_Y) == GPIO.HIGH:
                PiZero_Client.send(Pressed_Y)
                print('Yellow button was pressed, should send message')

            if received == True:
                break

            print("Y_button status: {} | G_button status: {}".format(GPIO.input(BUTTON_Y), GPIO.input(BUTTON_G)))

            time.sleep(1/2)
            
    except KeyboardInterrupt:
        print("Closing program via CTRL + C")

    finally:
        GPIO.cleanup()
