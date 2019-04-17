from bluedot.btcomm import BluetoothClient 
import time
import os
import sys
import RPi.GPIO as GPIO

received = False
# server_address(mulepizero in this case)= "B8:27:EB:87:A5:C2" 
# client address(james pi) = "B8:27:EB:38:7E:9C

#================== Pre-defined messages ================
Pressed_G = "G_PRESS"
Pressed_Y = "Y_PRESS"  # will make it activate comands later
#========================================================

BUTTON_G = 27
BUTTON_Y = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_G, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_Y, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def data_received(data):
    #print("received: ", data)
    c.send(data)
    global received
    received = True    

def ButtonCallback_G(channel):    
    PiZero_Client.send(Pressed_G)
     
def ButtonCallback_Y(channel):
    PiZero_Client.send(Pressed_Y)

GPIO.add_event_detect(BUTTON_G, GPIO.FALLING, callback=ButtonCallback_G, bouncetime=300)
GPIO.add_event_detect(BUTTON_Y, GPIO.FALLING, callback=ButtonCallback_Y, bouncetime=300)    

dist= 0
print("started")
orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

if __name__ == "__main__":

    PiZero_Client = BluetoothClient("jamespi", data_received)
    print("============= Starting bluetooth button activation test ============")
    try:
               
        while True:
            		            
            if GPIO.input(BUTTON_G) == GPIO.LOW:
                #PiZero_Client.send(Pressed_G)
                print('Green Press')
            elif GPIO.input(BUTTON_Y) == GPIO.LOW:
                #PiZero_Client.send(Pressed_Y)
                dist = dist + 5
                print('Yellow press at ', dist)
                

            if received == True:
                break

            #print(PiZero_Client.client_address)
            #os.system("hcitool rssi B8:27:EB:87:A5:C2")
            rssiMess = os.popen("hcitool rssi B8:27:EB:38:7E:9C").read()
            rssiVal = rssiMess[19:]
            print(rssiVal)	

            time.sleep(1/10)
            
    except KeyboardInterrupt:
        print("Closing program via CTRL + C")

    finally:
        GPIO.cleanup()
        sys.stdout = orig_stdout
        f.close()
