from bluedot.btcomm import BluetoothClient 
import time
import RPi.GPIO as GPIO

#================== Pre-defined messages ================
Pressed_BU = "DIST_10FT"
Pressed_Y = "DIST_5FT"  # will make it activate comands later
Pressed_B = "DIST_15FT"
Pressed_R = "STOP"
#========================================================

BUTTON_BU = 26 #26
BUTTON_Y = 22 #22
BUTTON_R = 17 #17
BUTTON_B = 27 #27
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_BU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_Y, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

received = False



def data_received(data):
    print("received: ", data)
    c.send(data)
    global received
    received = True


def ButtonCallback_G(channel):    
    PiZero_Client.send(Pressed_BU)
     
def ButtonCallback_Y(channel):
    PiZero_Client.send(Pressed_Y)

def ButtonCallback_W(channel):
    PiZero_Client.send(Pressed_R)

def ButtonCallback_B(channel):
    PiZero_Client.send(Pressed_B)

    
GPIO.add_event_detect(BUTTON_BU, GPIO.RISING, callback=ButtonCallback_G, bouncetime=300)
GPIO.add_event_detect(BUTTON_Y, GPIO.RISING, callback=ButtonCallback_Y, bouncetime=300)
GPIO.add_event_detect(BUTTON_R, GPIO.RISING, callback=ButtonCallback_W, bouncetime=300)
GPIO.add_event_detect(BUTTON_B, GPIO.RISING, callback=ButtonCallback_B, bouncetime=300)


if __name__ == "__main__":
    print("============= Starting bluetooth button activation test ============")
    PiZero_Client = BluetoothClient("jamespi", data_received)

    try:
        print("============= Starting bluetooth button activation test ============")
        PiZero_Client.send("Hello")

        while True:
            
            if GPIO.input(BUTTON_Y) == GPIO.LOW:               
                print('Yellow button was pressed, should send message')

            elif GPIO.input(BUTTON_BU) == GPIO.LOW:                
                print('Blue button was pressed, should send message')

            elif GPIO.input(BUTTON_R) == GPIO.LOW:
                print('Red button was pressed, should send message')

            elif GPIO.input(BUTTON_B) == GPIO.LOW:
                print('Black button was pressed, should send message')
            
            if received == True:
                break

            #print("Y_button status: {} | Bu_Button status: {} | R_Button status: {} | B_button status: {}".format(GPIO.input(BUTTON_Y), GPIO.input(BUTTON_BU), GPIO.input(BUTTON_R), GPIO.input(BUTTON_B)))
            #print("Y_Button status: {}".format(GPIO.input(BUTTON_Y)))
            #PiZero_Client.send(Pressed_G)
            time.sleep(1/2)
            
    except KeyboardInterrupt:
        print("Closing program via CTRL + C")

    finally:
        GPIO.cleanup()
