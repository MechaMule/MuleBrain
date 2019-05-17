from bluedot.btcomm import BluetoothClient
import time
import RPi.GPIO as GPIO

#===================== Predefined messages =======================
Detect = "FOUND"
Lost   = "LOST"
CornerLeft = False
CornerRight = False
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
    CornerLeft = False      #Reseting corner flags
    CornerRight = False
    
    # if statements check to see current values of IR sensors.
    # Depending on values, it lets us know if there is a corner or not
    # If GPIO.LOW then it means sensors have detected signal
    # If GPIO.HIGH then sensors have lost signal    
        
    if (GPIO.input(IR_L) == GPIO.HIGH) and (GPIO.input(IR_R) == GPIO.HIGH):
        print("{}_L_Callback".format(Both_Lost))
        CornerLeft = False
        CornerRight = False
        
    elif (GPIO.input(IR_L) == GPIO.HIGH) and (GPIO.input(IR_R) == GPIO.LOW):
        CornerRight = True
        print("{}_LEFT_L_Callback".format(Lost))
    #else:                               # Might not need this statument
        #PiZero_Client.send(Left_Lost)  # Because it is redudent with statement
       # print("{}_RIGHT_L_Callback".format(Lost))  # in IRR_Callback
        #CornerLeft = True


# IR sensor Interrupt for         
def IRR_Callback(channel):
    CornerLeft = False      # Reseting corner detection flag
    CornerRight = False

    # if statements check to see current values of IR sensors.
    # Depending on values, it lets us know if there is a corner or not
    # If GPIO.LOW then it means sensors have detected signal
    # If GPIO.HIGH then sensors have lost signal
    #Lost both sensors here, will wait to detect one of the sides.
    if (GPIO.input(IR_R) == GPIO.HIGH) and (GPIO.input(IR_L) == GPIO.HIGH):
        print("{}_R_Callback".format(Both_Lost))
        CornerLeft = False
        CornerRight = False
    
    elif (GPIO.input(IR_R) == GPIO.HIGH) and (GPIO.input(IR_L) == GPIO.LOW):
        print("{}_RIGHT_R_callback".format(Lost))
        CornerLeft = True
        
#    else:
#        print("{}_LEFT_R_Callback".format(Lost))
#        CornerRight = True


GPIO.add_event_detect(IR_L, GPIO.BOTH, callback=IRL_Callback, bouncetime=300)
GPIO.add_event_detect(IR_R, GPIO.BOTH, callback=IRR_Callback, bouncetime=300)

if __name__ == "__main__":
    print("==================== Starting IR Message Test =====================")
    C_left = 0
    C_Right = 0

    try:
        
        while True:

            # Shows us the status of the IR sensors in real semi-real time.
            if CornerLeft:
                C_left = 1
            else:
                C_left = 0

            if CornerRight:
                C_Right = 1
            else:
                C_right = 0
                
            print("LeftSensor: {} | RightSensor: {}".format(C_left, C_Right))
            print("L_Status:   {} | R_Status:    {}".format( GPIO.input(IR_L),  GPIO.input(IR_R) ))
            # Slight delay to releave the processor of any stress. 
            time.sleep(1/2)


    except KeyboardInterrupt:
        print("Closing program via CTRL + C")

    finally:
        GPIO.cleanup((IR_L, IR_R))

    
