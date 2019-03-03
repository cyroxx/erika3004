#include <SoftwareSerial.h>
#include "ddr2ascii.h"
#include "ascii2ddr.h"

#define PC_BAUD 9600

#define RTS_PIN 3
#define ERIKA_RX 10
#define ERIKA_TX 11
#define ERIKA_BAUD 1200

SoftwareSerial erika(ERIKA_RX, ERIKA_TX); // RX, TX
bool wait = false;

void setup()
{
	pinMode(RTS_PIN, INPUT);
	Serial.begin(PC_BAUD);
	erika.begin(ERIKA_BAUD);
}

void loop()
{ // run over and over
	int rtsState = digitalRead(RTS_PIN);

	//continue on falling edge
	if (rtsState == LOW && wait == false)
	{
		//data from pc in serial buffer ?
		if (Serial.available())
		{
			//convert to raw (ddr-ascii)
			int result = ascii2ddr[Serial.read()];
			erika.write(result);
			//Serial.println(result,HEX);
			//wait until rts went high
			wait = true;
		}
	}
	else //if (val == HIGH)
	{
		//rts was high, which means erika is ready for the next byte, when rts goes low again
		wait = false;
	}
	//erika has data to send
	if (erika.available())
	{
		//convert ddr-ascci to ascii and send to pc
		Serial.write(ddr2ascii[erika.read()]);
	}
}
