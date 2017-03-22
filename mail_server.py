#!/usr/bin/env python2.7
# Sean Newman
import socket as sck

HOST = ''
PORT = 10101

sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

print 'connected to ', addr

conn.sendall('Connected successfully.')
conn.close()
