#!/usr/bin/env python2.7
# Sean Newman
import socket as sck
from datetime import datetime

HOST = '127.0.0.1'
PORT = 10101

# create socket
sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
sock.connect((HOST, PORT))
data = sock.recv(1024)
print data
sock.sendall('HELO relay.mydomain.cars')
data = sock.recv(1024)
print data

# get the sender
sender = raw_input('Sending email address: ')
sock.sendall('MAIL FROM:<', sender, '>')
data = sock.recv(1024)
print data

# get recipients
rcpts = []
getting = True
while getting:
    new_rcpt = raw_input('Would you like to add another recipient? (Y/N): ')
    if new_rcpt == 'Y':
        recipient = raw_input('Recipient email address: ')
        sock.sendall('RCPT TO:<', recipient, '>')
        data = sock.recv(1024)
        print data
        rcpts.append(recipient)
    elif new_rcpt == 'N':
        getting == False

# make the email
sock.sendall('DATA')
sock.recv(1024)
print data

sock.sendall('From: "', raw_input('Full name of ', sender), '" <', sender, '>')

for rcpt in rcpts:
    sock.sendall('To: "', raw_input('Full name of', rcpt), '" <', rcpt, '>')

sock.sendall('Date: ', datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'))

making_email = True
print 'Type "END" to end email.'
while making_email:
    line = raw_input('>')
    if line == 'END':
        making_email = False
        sock.sendall('.')
    else:
        sock.sendall(line)
        data = sock.recv(1024)
        print data

sock.sendall(line)
data = sock.recv(1024)
print data

sock.close()
