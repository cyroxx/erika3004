from serial.tools import miniterm
import erika.codec as erika_codec
import codecs

codecs.register(lambda c: erika_codec.getregentry() if c == 'erika3004' else None)

if __name__ == '__main__':
    miniterm.main(default_port='/dev/ttyAMA0', default_baudrate=1200, default_rts=True)
