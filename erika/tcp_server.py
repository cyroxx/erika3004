#!/usr/bin/env python3

import socket
import string

TCP_IP = '127.0.0.1'
TCP_PORT = 2227
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

ALLOWED_CHARACTERS = string.digits + string.ascii_letters + "@.,;:# ()_/?!\"§+%&=*-'äöüÄÖÜßéè°|$£µ^²³"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    print('Connection address:', addr)
    data = conn.recv(BUFFER_SIZE)

    try:
        sanitized_tweet = data.decode('utf-8')
        sanitized_tweet = ''.join(c for c in sanitized_tweet if c in ALLOWED_CHARACTERS)
        sanitized_tweet = sanitized_tweet.replace('@', "(at)")

        print("sanitized data:", sanitized_tweet)
        conn.send(data)  # echo
    except UnicodeDecodeError as e:
        conn.send("Invalid bytes. You must send UTF-8.\n".encode("utf-8"))
        print("Invalid bytes", e)
    finally:
        conn.close()
