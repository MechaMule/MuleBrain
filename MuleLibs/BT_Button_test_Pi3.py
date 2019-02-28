from bluedot.btcomm import BluetoothServer
import Signal
import time
import RPi.GPIO as GPIO

LED_Y = 25
LED_G = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_Y, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_G, GPIO.OUT, initial=GPIO.LOW)

def data_received(data):
    print("Received", data)
    global save_msg         # Need access to the message so I made it a global
    save_msg = data         # There may be a way to save message through a function call
                            # that is external to the data_received() function
                            # I'll try that tomorrow.w
save_msg = "Nothing meaningful"
Server = BluetoothServer(data_received)


try:
    print("=================Starting test=====================")

    while True:
        #print('Saved string: {}'.format(Save_Str))
        if save_msg == 'DIST_5FT':
            print("Going to Distance options")
            GPIO.output(LED_G, GPIO.HIGH)
            save_msg = "Cleared Previous G Message"
            
        elif save_msg == 'DIST_10FT':
            print("Going to Calibration settings")
            GPIO.output(LED_Y, GPIO.HIGH)
            save_msg = "Cleared Previous Y Message"
        else:
            GPIO.output(LED_Y, GPIO.LOW)
            GPIO.output(LED_G, GPIO.LOW)
        print (save_msg)
        time.sleep(1/2)
except KeyboardInterrupt:
    print("Exiting program via CTRL + C")

finally:
    GPIO.cleanup()
