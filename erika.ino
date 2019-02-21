
#include <SoftwareSerial.h>

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

char ddr2ascii [128] = {
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
'2',
'1',
'H',
':',
'D',
'²',
'M',
'\"',
'B',
'^',
'Q',
'*',
'G',
'(',
'O',
')',
'C',
'I',
'V',
'³',
'K',
'+',
'X',
'|',
'U',
' ',
'N',
'`',
'L',
'W',
'=',
'P',
'A',
'Y',
'J',
'S',
'E',
'?',
'R',
'T',
'Z',
'°',
'Ü',
';',
'Ö',
'§',
'F',
'Ä',
'/',
'#',
'!',
'"',
'é',
'ç',
'è',
'ß',
'$',
'f',
'm',
'j',
'w',
'l',
'b',
'v',
'k',
'y',
'q',
'd',
'z',
'h',
't',
'c',
's',
'r',
'e',
'p',
'n',
'u',
'o',
'x',
'g',
'a',
'-',
'.',
',',
'ä',
'ö',
'ü',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
'\n',
' ',
' ',
' ',
' ',
' ',
' ',
' ',
' '};

char ascii2ddr [128] = {
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x91,
0x77,
0x71,
0x71,
0x92,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x71,
0x42,
0x43,
0x41,
0x48,
0x04,
0x02,
0x17,
0x1D,
0x1F,
0x1B,
0x25,
0x64,
0x62,
0x63,
0x40,
0x0D,
0x11,
0x10,
0x0F,
0x0E,
0x0C,
0x0B,
0x0A,
0x09,
0x08,
0x13,
0x3B,
0x71,
0x2E,
0x71,
0x35,
0x71,
0x30,
0x18,
0x20,
0x14,
0x34,
0x3E,
0x1C,
0x12,
0x21,
0x32,
0x24,
0x2C,
0x16,
0x2A,
0x1E,
0x2F,
0x1A,
0x36,
0x33,
0x37,
0x28,
0x22,
0x2D,
0x26,
0x31,
0x38,
0x71,
0x71,
0x71,
0x19,
0x01,
0x2B,
0x61,
0x4E,
0x57,
0x53,
0x5A,
0x49,
0x60,
0x55,
0x05,
0x4B,
0x50,
0x4D,
0x4A,
0x5C,
0x5E,
0x5B,
0x52,
0x59,
0x58,
0x56,
0x5D,
0x4F,
0x4C,
0x5F,
0x51,
0x54,
0x71,
0x27,
0x71,
0x71,
0x71
};

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

//char ddr2ascii(char val)
//{
//  switch(val)
//  {
//    case 'a':
//     return '';
//    case 'b':
//    return '';
//  }
//}
//
//char ascii2ddr(char val)
//{
//}
//}
