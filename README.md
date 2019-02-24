# Erika3004

## Encoding

The Erika3004 Typewriter uses a prorietary encoding, which is NOT compatible with ASCII, Unicode, etc.
Therefore software is needed to convert the RAW encoding (or DDR-ASCII ;) ) to something more usefull like ASCII.
A table of all available characters and their hex value can be found in this manual( [Erika-IF2014_AnwenderHandbuch](Erika-IF2014_AnwenderHandbuch.pdf) ) as Appendix E on page 10. It also has a list of the most used controll characters on page 11 (Appendix F). A complete list can be found [here](http://hc-ddr.hucki.net/wiki/doku.php/z9001/erweiterungen/s3004).
We implemented the conversion in python using a json-file which contains all characters and their hex-value.
The implementation for Arduino uses hardcoded arrays instead.

## Hardware

Description of the Erica connector:
![Erika Connector](http://hc-ddr.hucki.net/wiki/lib/exe/fetch.php/z9001/erweiterungen/s3004_anschluss.jpg?cache=)

More infos can be found here (German): [http://hc-ddr.hucki.net/wiki/doku.php/z9001/erweiterungen/s3004](http://hc-ddr.hucki.net/wiki/doku.php/z9001/erweiterungen/s3004)

A schematic of our Arduino based interface can be found [here](https://easyeda.com/editor#id=708dfbb12ec9406986608b1bfc6e0a6b).
![Schematic](Schematic_ErikaArduinoInterface_Sheet-1_20190224110903.png)

## Software

### Arduino Sketch

The arduino sketch should be compilable for any Arduino that has at least one hardware UART (hardware serial).
TODO: Test on Mini, Nano
The arduino will comunicate with your pc using the default hardware serial, which is usually connected to a usb to serial converter.
It will use a software serial to communicate with the Erika3004.
More information about SoftwareSerial can be found on the [Arduino-Website](https://www.arduino.cc/en/Reference/SoftwareSerial).
In `erika.ino` you can set the following constants:

> Remember: Serial connections are connected with cross-over. This means RX on the Arduino connects to TX on the Erika and vice versa.

|Name|Description|Default Value|Comment|
|----|-----------|-------------|-------|
|PC_BAUD| Baudrate used to communicate with the pc|9600|You can change this to fit your needs.|
|RTS_PIN| Pin that is connected to the ready to send pin of the Erika.|3|You can change this to any available digital input pin on your arduino.|
|ERIKA_RX| Recieve pin of the SoftwareSerial to communicate with Erika.|10|Check the limitations section on the  [Arduino-Website](https://www.arduino.cc/en/Reference/SoftwareSerial), to find out which pins can be used by SoftwareSerial.|
|ERIKA_TX| Transmit pin of the SoftwareSerial to communicate with Erika.|11|Check the limitations section on the  [Arduino-Website](https://www.arduino.cc/en/Reference/SoftwareSerial), to find out which pins can be used by SoftwareSerial.|
|ERIKA_BAUD| Baudrate used by the Erika3004.|1200|DON'T CHANGE THIS! The Erika3004 will only work with 1200 Baud!|

Translation from ASCII to DDR-ASCII is done using arrays defined in `ddr2ascii.h` and `ascii2ddr.h` .
