from bluedot.btcomm import BluetoothClient
import time
import RPi.GPIO as GPIO

#===================== Predefined messages =======================
Detect = "FOUND"
Lost   = "LOST"
CornerLeft = 0
CornerRight = 0
Both_Detect  = "BOTH_FOUND"
Both_Lost    = "BOTH_LOST"
#=================================================================

IR_L = 17
IR_R = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_L, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IR_R, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

received = False

# For now the callbacks have print statements to check to see if they
#are being accessed
def IRL_Callback(channel):
    global CornerLeft
    global CornerRight
    CornerLeft = 0      #Reseting corner flags
    CornerRight = 0
        
    if (GPIO.input(IR_L) == GPIO.HIGH) and (GPIO.input(IR_R) == GPIO.HIGH):
        CornerLeft = 0
        CornerRight = 0
        
    elif (GPIO.input(IR_L) == GPIO.HIGH) and (GPIO.input(IR_R) == GPIO.LOW):
        CornerRight = 1
        
    else:                               # Might not need this statument
        CornerLeft = 1


# IR sensor Interrupt for         
def IRR_Callback(channel):
    global CornerLeft
    global CornerRight
    CornerLeft = 0      # Reseting corner detection flag
    CornerRight = 0

    # if statements check to see current values of IR sensors.
    # Depending on values, it lets us know if there is a corner or not
    # If GPIO.LOW then it means sensors have detected signal
    if (GPIO.input(IR_R) == GPIO.HIGH) and (GPIO.input(IR_L) == GPIO.HIGH):
        CornerLeft = 0
        CornerRight = 0
    
    elif (GPIO.input(IR_R) == GPIO.HIGH) and (GPIO.input(IR_L) == GPIO.LOW):
        CornerLeft = 1
        
    else:
        CornerRight = 1
# Function that returns the states of the IR Receivers.
# Values are updated when interrupt is triggered

def GetIR_States():
    global CornerLeft
    global CornerRight
    IR_states = ((CornerLeft << 1) & 0b10) | (CornerRight & 0b01)
    return IR_states


GPIO.add_event_detect(IR_L, GPIO.BOTH, callback=IRL_Callback, bouncetime=300)
GPIO.add_event_detect(IR_R, GPIO.BOTH, callback=IRR_Callback, bouncetime=300)

if __name__ == "__main__":
    print("==================== Starting IR Message Test =====================")

    try:
        
        while True:

            # Shows us the status of the IR sensors in real semi-real time.
            #print("L_Status: {} | R_Status: {}".format( GPIO.input(IR_L),  GPIO.input(IR_R) ))
            # Slight delay to releave the processor of any stress.
            print (GetIR_States())
            time.sleep(1/2)


    except KeyboardInterrupt:
        print("Closing program via CTRL + C")

    finally:
        GPIO.cleanup((IR_L, IR_R))

    
