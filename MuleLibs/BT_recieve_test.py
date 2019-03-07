from bluedot.btcomm import BluetoothServer
import Signal
import time




def data_received(data):
    print("Received", data)
    global save_msg         # Need access to the message so I made it a global
    save_msg = data         # There may be a way to save message through a function call
                            # that is external to the data_received() function
save_msg = "Nada"           # I'll try that tomorrow.w

Server = BluetoothServer(data_received)

try:
    print("=================Starting test=====================")

    while True:
        #print('Saved string: {}'.format(Save_Str))
        if save_msg == 'PING':
            print("PING here")
            
        elif save_msg == "PONG":
            print("PONG here")

        else:
            print(save_msg)
			            
        #print (save_msg)
        time.sleep(1/2)
except KeyboardInterrupt:
    print("Exiting program via CTRL + C")

#finally:
#    GPIO.cleanup()

