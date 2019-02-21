#include <SoftwareSerial.h>
#include "ddr2ascii.h"
#include "ascii2ddr.h"

SoftwareSerial mySerial(10, 11); // RX, TX
int inPin = 3;


void setup() {
  // Open serial communications and wait for port to open:
  pinMode(inPin, INPUT);
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


  Serial.println('Goodnight moon!');

  // set the data rate for the SoftwareSerial port
  mySerial.begin(1200);
}
bool wait = false;





void loop() { // run over and over
   int val = digitalRead(inPin);
   //Serial.println(val);
    if(val == LOW && wait == false)
     {
          if (Serial.available()) {
            int result = ascii2ddr[Serial.read()];
            mySerial.write(result);
            Serial.println(result,HEX);
            wait = true;
           } 
     }
     else if (val == HIGH){
        wait = false;
     }
     if(mySerial.available()){
      Serial.write(ddr2ascii[mySerial.read()]);
     }

}

