import re

ESC = "\x1B"  # = "\033" # = "\x1B" #
CSI = ESC + "["

csi_codes = {
    "A": lambda n: "Cursor Up ({})".format(n)
    , "B": lambda n: "Cursor Down ({})".format(n)
    , "C": lambda n: "Cursor Forward ({})".format(n)
    , "D": lambda n: "Cursor Back ({})".format(n)
    , "E": lambda n: "Cursor Next Line ({})".format(n)
    , "F": lambda n: "Cursor Previous Line ({})".format(n)
    , "G": lambda n: "Cursor Horizontal Absolute ({})".format(n)
    , "H": lambda n, m: "Cursor Position ({n}, {m})".format(n, m)
    , "J": "Erase in Display"
    , "K": "Erase in Line"
    , "S": "Scroll Up"
    , "T": "Scroll Down"
    , "f": "Horizontal Vertical Position"
    , "m": lambda *n: "Select Graphic Rendition {}".format([sgr_codes.get(x) for x in n])
    , "i": "AUX Port"
    , "n": "Device Status Report"
    , "s": "Save Cursor Position"
    , "u": "Restore Cursor Position"
}

sgr_codes = {
    "0": "reset"
    , "1": "bold"
    , "2": "faint"
    , "3": "italic"
    , "4": "underline"
    , "5": "slow blink"
    , "6": "rapid blink"
    , "31": "foreground red"
}


def find_seq(string):
    # this regex matches on ANSI escape sequences
    esc_seq_regex = "\x1B\\[((?:[0-9]?;?)*[\x40-\x7E])"  # "\x1B\\[([0-9]?;?)*[\x40-\x7E]"

    # make sure there are no unsupported escape sequences
    check = re.sub(esc_seq_regex, "", string)
    assert ESC not in check, "unsupported escape sequence found"

    # find all escape sequences
    escape_sequences = re.findall(esc_seq_regex, string)
    # replace them with just the ESC character
    string = re.sub(esc_seq_regex, ESC, string)

    for c in string:
        if c == ESC:
            print(decode_escape_sequence(escape_sequences.pop(0)))
        else:
            print(c)


def decode_escape_sequence(seq):
    command = seq[-1]
    params = seq[:-1].split(";")
    return csi_codes[command](*params)


if __name__ == "__main__":
    find_seq("\033[31;1;4mHello\033[0m\033[10A")
    find_seq("\033[10AHallo")
