from bluedot.btcomm import BluetoothClient 
import time
import RPi.GPIO as GPIO

#================== Pre-defined messages ================
Pressed_G = "DIST_10FT"
Pressed_Y = "DIST_5FT"  # will make it activate comands later
Pressed_W = "DIST_15FT"
Pressed_B = "STOP"
#========================================================

BUTTON_G = 27
BUTTON_Y = 17
BUTTON_W = 26
BUTTON_B = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_G, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_Y, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_W, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

received = False



def data_received(data):
    print("received: ", data)
    c.send(data)
    global received
    received = True


def ButtonCallback_G(channel):    
    PiZero_Client.send(Pressed_G)
     
def ButtonCallback_Y(channel):
    PiZero_Client.send(Pressed_Y)

def ButtonCallback_W(channel):
    PiZero_Client.send(Pressed_W)

def ButtonCallback_B(channel):
    PiZero_Client.send(Pressed_B)

    
GPIO.add_event_detect(BUTTON_G, GPIO.FALLING, callback=ButtonCallback_G, bouncetime=300)
GPIO.add_event_detect(BUTTON_Y, GPIO.FALLING, callback=ButtonCallback_Y, bouncetime=300)
GPIO.add_event_detect(BUTTON_W, GPIO.FALLING, callback=ButtonCallback_W, bouncetime=300)
GPIO.add_event_detect(BUTTON_B, GPIO.FALLING, callback=ButtonCallback_B, bouncetime=300)


if __name__ == "__main__":

    PiZero_Client = BluetoothClient("johnpi", data_received)

    try:
        print("============= Starting bluetooth button activation test ============")
        

        while True:
            
            if GPIO.input(BUTTON_G) == GPIO.HIGH:               
                print('Green button was pressed, should send message')
            elif GPIO.input(BUTTON_Y) == GPIO.HIGH:
                
                print('Yellow button was pressed, should send message')

            elif GPIO.input(BUTTON_W) == GPIO.HIGH:
                print('White button was pressed, should send message')

            elif GPIO.input(BUTTON_B) == GPIO.HIGH:
                print('Black button was pressed, should send message')
            
            if received == True:
                break

            print("Y_button status: {} | G_button status: {} | W_button status: {} | B_button status: {}".format(GPIO.input(BUTTON_Y), GPIO.input(BUTTON_G), GPIO.input(BUTTON_W), GPIO.input(BUTTON_B)))

            time.sleep(1/2)
            
    except KeyboardInterrupt:
        print("Closing program via CTRL + C")

    finally:
        GPIO.cleanup()
