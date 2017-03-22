#!/usr/bin/env python2.7
# Sean Newman
import socket as sck

HOST = '127.0.0.1'
PORT = 10101

sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
sock.connect((HOST, PORT))
print sock.recv(1024)
sock.close()
