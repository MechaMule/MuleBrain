/*================================================= 
  File: 
  Date: 04/13/2019
  By: Johnson Le
  Desc: Mule's Receiver Controller
/*=================================================
 * Libraries 
==================================================*/
#include <RF24.h>

/*=================================================
 * Defines
==================================================*/
#define PIN_CE 3
#define PIN_CSN 4
#define address_R 0xABCDEF

RF24 nrf(PIN_CE, PIN_CSN);
char msg[64];
unsigned long rec;
int msg_len = 0;

void setup() {
    nrf.begin();
    nrf.enableDynamicPayloads();
    nrf.setRetries(15, 15);
    nrf.openReadingPipe(1, address_R);
    nrf.startListening();
}

void loop() {
    if(nrf.available()){
        while(nrf.available()){
            nrf.read(&rec , sizeof(unsigned long));
        }
    }
}
