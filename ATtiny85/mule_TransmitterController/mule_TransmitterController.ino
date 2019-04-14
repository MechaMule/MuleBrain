/*================================================= 
  File: 
  Date: 04/11/2019
  By: Johnson Le
  Desc: Mule's Transmitter Controller
/*=================================================
 * Libraries 
==================================================*/
#include <RF24.h>

/*==================================================
 * Defines 
==================================================*/
#define PIN_CE 3
#define PIN_CSN 4
#define address_T 0xABCDEF

RF24 nrf(PIN_CE, PIN_CSN);
static char msg[] = "g";
unsigned long sen = 4;

/*==================================================
 * Setup 
==================================================*/
void setup() {
    nrf.begin();
    nrf.enableDynamicPayloads();
    nrf.setRetries(15, 15);
    nrf.openWritingPipe(address_T);
}
/*==================================================
 * Main Loop
==================================================*/
void loop() {
    nrf.write(msg, strlen(msg));
//    nrf.write(&sen, sizeof(unsigned long));
    delay(200);
}
