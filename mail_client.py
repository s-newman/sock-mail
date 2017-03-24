#!/usr/bin/env python2.7
# Sean Newman
import socket as sck
from datetime import datetime
from mail_comms import *

HOST = '127.0.0.1'
PORT = 10101

def send_print(sock, data):
    sock.sendall(data)
    print 'CLIENT: ' + data

def recv_print(sock):
    data = sock.recv(1024)
    print 'SERVER: ' + data

def send_recv(sock, data):
    send_print(sock, data)
    recv_print(sock)

def main():
    # create socket
    sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    sock.connect((HOST, PORT))
    recv_print(sock)
    send_recv(sock, 'HELO relay.mydomain.cars')

    # get the sender
    sender = raw_input('Sending email address: ')
    send_recv(sock, 'MAIL FROM:<' + str(sender) + '>')

    # get recipients
    rcpts = []
    getting = True
    while getting:
        new_rcpt = raw_input('Would you like to add another recipient? (Y/N): ')
        if new_rcpt == 'Y':
            recipient = raw_input('Recipient email address: ')
            send_recv(sock, 'RCPT TO:<' + str(recipient) + '>')
            rcpts.append(recipient)
        elif new_rcpt == 'N':
            break

    # send the sender header
    send_recv(sock, 'DATA')

    send_print(sock,
            'From: "' + str(raw_input('Full name of ' + sender + ': ')) +
            '" <' + str(sender) + '>')

    # send the recipients header(s)
    for rcpt in rcpts:
        send_print(sock,
            'To: "' + str(raw_input('Full name of ' + rcpt + ': ')) +
            '" <' + str(rcpt) + '>')

    # send the time header
    send_print(sock, 'Date: ' + datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'))

    making_email = True
    print 'Type "END" to end email.'
    while making_email:
        line = raw_input('>')
        if line == 'END':
            making_email = False
            send_recv(sock, '.')
        else:
            sock.sendall(line)

    send_recv(sock, 'QUIT')
    sock.close()

if __name__ == '__main__':
    main()

