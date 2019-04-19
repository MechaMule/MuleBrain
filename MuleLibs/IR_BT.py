from bluedot.btcomm import BluetoothClient
import time
import RPi.GPIO as GPIO

#===================== Predefined messages =======================
Left_Detect = "SIGNAL_FOUND_L"
Left_Lost   = "SIGNAL_LOST_L"

Right_Detect = "SIGNAL_FOUND_R"
Right_Lost   = "SIGNAL_LOST_R"

Both_Detect  = "BOTH_FOUND"
Both_Lost    = "BOTH_LOST"
#=================================================================

IR_L = 17
IR_R = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_L, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IR_R, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

received = False

def data_received(data):
    print("received: ",data)
    c.send(data)
    global received
    received = True

# For now the callbacks have print statements to check to see if they
#are being accessed
def IRL_Callback(channel):
    if (GPIO.input(IR_L) == GPIO.LOW) and (GPIO.input(IR_R) == GPIO.LOW):
        #PiZero_Client.send(Both_Detect)
        print('Found_BOTH_L_Callback')
        
    elif (GPIO.input(IR_L) == GPIO.HIGH) and (GPIO.input(IR_R) == GPIO.HIGH):
        print('Lost BOTH_L_Callback')
        
    elif (GPIO.input(IR_L) == GPIO.HIGH) and (GPIO.input(IR_R) == GPIO.LOW):       #Need to do a check for both HIGH and then move this statement down the
        #PiZero_Client.send(Left_Detect)        #of if statements
        print('Lost LEFT_L_Callback')
    else:
        #PiZero_Client.send(Left_Lost)
        print('Lost_RIGHT_L_Callback')

        
def IRR_Callback(channel):
    if (GPIO.input(IR_R) == GPIO.LOW) and (GPIO.input(IR_L) == GPIO.LOW):
        #PiZero_Client.send(Both_Detect)
        print('Found BOTH_R_Callback')

    elif (GPIO.input(IR_R) == GPIO.HIGH) and (GPIO.input(IR_L) == GPIO.HIGH):
        print('Lost BOTH_R_Callback')
    
    elif (GPIO.input(IR_R) == GPIO.HIGH) and (GPIO.input(IR_L) == GPIO.LOW):
        #PiZero_Client.send(Right_Detect)
        print('Lost RIGHT_R_callback')
        
    else:
        #PiZero_Client.send(Right_Lost)
        print('Lost LEFT_R_Callback')


GPIO.add_event_detect(IR_L, GPIO.BOTH, callback=IRL_Callback, bouncetime=300)
GPIO.add_event_detect(IR_R, GPIO.BOTH, callback=IRR_Callback, bouncetime=300)

if __name__ == "__main__":
    print("==================== Starting IR Message Test =====================")
#    PiZero_Client = BluetoothClient("johnpi", data_received)

    try:
        
        while True:
#            #Signals are inverted 
#            if (GPIO.input(IR_L) == GPIO.LOW) and (GPIO.input(IR_R) == GPIO.LOW):
#                print('Both sensors found signal')
#            
#            elif GPIO.input(IR_L) == GPIO.LOW:            
#                print('Only left found signal(HIGH), should send message') #these are
#                
#            elif GPIO.input(IR_R) == GPIO.LOW:
#                print('Only right found signal(HIGH), message sent')
#                
#            else:
#                print('Both lost signal')
            #This displays the status of booth sensors 
            print("L_Status: {} | R_Status: {}".format( GPIO.input(IR_L),  GPIO.input(IR_R)))

            time.sleep(1/2)


    except KeyboardInterrupt:
        print("Closing program via CTRL + C")

    finally:
        GPIO.cleanup((IR_L, IR_R))

    
