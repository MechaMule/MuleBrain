#!/usr/bin/env python
import serial
import time

port = "/dev/ttyACM0"
rate = 57600
startMarker = 60
endMarker = 62


s1 = serial.Serial(port, rate)

#8========================================================================D
def sendToArduino(sendStr):
    s1.write(sendStr.encode('utf-8'))

#8=======================================================================D

def recvFromArduino():
    global startMarker, endMarker

    ck = ""
    raw_Data = "z" # any value that is not an end- or startMarker
    byteCount = -1 # to allow for the fact that the last increment will be one too many

    # wait for the start character
    while  ord(raw_Data) != startMarker:
        raw_Data = s1.read()

    # save data until the end marker is found
    while ord(raw_Data) != endMarker:
        if ord(raw_Data) != startMarker:
            ck = ck + raw_Data.decode("utf-8") 
            byteCount += 1
        raw_Data = s1.read()

    return(ck)


#8======================================================================D

def waitForArduino():

    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

    global startMarker, endMarker

    msg = ""
    while msg.find("Arduino is ready") == -1:

        while s1.inWaiting() == 0:
            pass

        msg = recvFromArduino()

        print (msg) 
        print ()

#8========================================================================D

def runTest(td):
    numLoops = len(td)
    waitingForReply = False

    n = 0
    while n < numLoops:
        teststr = td[n]

        if waitingForReply == False:
            sendToArduino(teststr)
            print ("Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + teststr)
            waitingForReply = True

        if waitingForReply == True:

            while s1.inWaiting() == 0:
                pass

            dataRecvd = recvFromArduino()
            print ("Reply Received  " + dataRecvd)
            n += 1
            waitingForReply = False

            print ("===========")

        time.sleep(1)


#======================================


if __name__ == '__main__':
    try: 
        print ("Serial port " + port + " opened  Baudrate " + str(rate))




        waitForArduino()


        testData = []
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        testData.append("<REVS>")
        
        runTest(testData)

    except KeyboardInterrupt:
        s1.close
        print("Closed by Ctrl+C")
