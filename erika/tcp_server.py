#!/usr/bin/env python3

import socket
import string

TCP_IP = '127.0.0.1'
TCP_PORT = 2227
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response


def sanitize_tweet(tweet_as_string):
    allowed_characters = string.digits + string.ascii_letters + "@.,;:# ()_/?!\"§+%&=*-'äöüÄÖÜßéè°|$£µ^²³"
    sanitized_tweet = tweet_as_string
    sanitized_tweet = ''.join(c for c in sanitized_tweet if c in allowed_characters)
    sanitized_tweet = sanitized_tweet.replace('@', "(at)")

    return sanitized_tweet


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    print('Connection address:', addr)
    data = conn.recv(BUFFER_SIZE)
    print("received data:", data)
    print("sanitized data:", sanitize_tweet(data))
    conn.send(data)  # echo
    conn.close()
