#!/usr/bin/env python2.7
# Sean Newman
import socket as sck
from mail_comms import *

HOST = ''
PORT = 10101
QUEUE = 0

sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(3)  # allow a few people to connect and wait

# accept a connection
while True:
    from_addr = ''
    to_addr = []
    content = ''

    conn, addr = sock.accept()
    print 'connected to ', addr

    send_print(conn, '200 mail.rit.edu ESMTP Postfix', server=True)
    connected = True

    # handle each command
    while connected:
        data = recv_print(conn, server=True)
        
        if data[0] == 'HELO':
            send_print(conn, '250 Hello ' + data[1] +
                    ', I am glad to meet you', server=True)

        elif data[0] == 'MAIL':
            addr_start = data[1].find('<')
            addr_end = data[1].find('>')
            from_addr = data[1][addr_start + 1 : addr_end]
            send_print(conn, '250 Ok', server=True)

        elif data[0] == 'RCPT':
            addr_start = data[1].find('<')
            addr_end = data[1].find('>')
            from_addr = data[1][addr_start + 1 : addr_end]
            send_print(conn, '250 Ok', server=True)

        elif data[0] == 'DATA':
            send_print(conn, '354 End data with <CRLF>.<CRLF>', server=True)
            record = True
            while record:
                entry = conn.recv(1024)
                print entry
                if entry == '.':
                    record = False
                    QUEUE += 1
                    send_print(conn, '250 Ok: queued as ' + str(QUEUE),
                            server=True)
                else:
                    content += entry
            
        elif data[0] == 'QUIT':
            send_print(conn, '221 Bye', server=True)
            conn.close()
            connected = False

