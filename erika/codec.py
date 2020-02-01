from __future__ import absolute_import

import codecs
import serial

from .erica_encoder_decoder import DDR_ASCII


try:
    unicode
except (NameError, AttributeError):
    unicode = str       # for Python 3, pylint: disable=redefined-builtin,invalid-name


HEXDIGITS = '0123456789ABCDEF'

ddr_codec = DDR_ASCII()
# Codec APIs

def hex_encode(data, errors='strict'):
    """'40 41 42' -> b'@ab'"""
    return (serial.to_bytes([int(h, 16) for h in data.split()]), len(data))

def erika_encode(data, errors='strict'):
    """'abc' -> """
    print(data)

    # use translation table -> list of hex strings ['61', '4E', '57']
    hexstr = [ddr_codec.encode(c) for c in data]

    return (bytes.fromhex(''.join(hexstr)), len(hexstr))


def erika_decode(data, errors='strict'):

    # get list of hex strings
    hexstr = ['{:02X}'.format(b) for b in data]

    return (''.join([ddr_codec.decode(b) for b in hexstr]), len(hexstr))



def hex_decode(data, errors='strict'):
    """b'@ab' -> '40 41 42'"""
    return (unicode(''.join('{:02X} '.format(ord(b)) for b in serial.iterbytes(data))), len(data))


class Codec(codecs.Codec):
    def encode(self, data, errors='strict'):
        """'40 41 42' -> b'@ab'"""
        return erika_encode(data)

    def decode(self, data, errors='strict'):
        """b'@ab' -> '40 41 42'"""
        return erika_decode(data)


class IncrementalEncoder(codecs.IncrementalEncoder):
    """Incremental hex encoder"""

    def __init__(self, errors='strict'):
        self.errors = errors
        self.state = 0

    def reset(self):
        self.state = 0

    def getstate(self):
        return self.state

    def setstate(self, state):
        self.state = state

    def encode(self, data, final=False):
        """\
        Incremental encode, keep track of digits and emit a byte when a pair
        of hex digits is found. The space is optional unless the error
        handling is defined to be 'strict'.
        """
        return erika_encode(data)


class IncrementalDecoder(codecs.IncrementalDecoder):
    """Incremental decoder"""
    def decode(self, data, final=False):
        return erika_decode(data)


class StreamWriter(Codec, codecs.StreamWriter):
    """Combination of hexlify codec and StreamWriter"""


class StreamReader(Codec, codecs.StreamReader):
    """Combination of hexlify codec and StreamReader"""


def getregentry():
    """encodings module API"""
    return codecs.CodecInfo(
        name='hexlify',
        encode=erika_encode,
        decode=erika_decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamwriter=StreamWriter,
        streamreader=StreamReader,
        #~ _is_text_encoding=True,
    )


if __name__ == '__main__':
    codecs.register(lambda c: getregentry() if c == 'hexlify' else None)

    enc = codecs.encode('abc', 'hexlify')
    print(enc)

    dec = codecs.decode(enc, 'hexlify')
    print(dec)

    #enc = codecs.encode('abc', 'utf-8')
    #print(enc)
