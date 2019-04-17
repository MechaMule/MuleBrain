from bluedot.btcomm import BluetoothServer
import Signal
import time
import RPi.GPIO as GPIO

def data_received(data):
    print("Received", data)
    global save_msg
    save_msg = data

save_msg = "Nonthing meaningful"
Server = BluetoothServer(data_received)

try:
    print("==================== Starting Test =====================")

    while True:
        if save_msg == '':
            print("Corner/obstacle detected left") # Lost signal Left, either corner or obstacle detected
        elif save_msg == '':
            print("Corner/obstacle detected right") # found obstacle/corner right side

        elif save_msg == '':
            print("Target located in front")

        print(save_msg)
        time.sleep(1/2)

except KeyboardInterrupt:
    print("Exiting program via CTRL+C")


