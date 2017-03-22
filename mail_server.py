#!/usr/bin/env python2.7
# Sean Newman
import socket as sck

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

    conn.sendall('200 mail.rit.edu ESMTP Postfix')
    connected = True

    # handle each command
    while connected:
        data = conn.recv(1024).strip().split()
        
        if data[0] == 'HELO':
            conn.sendall('250 Hello ' + data[1] + ', I am glad to meet you')

        elif data[0] == 'MAIL':
            addr_start = data[1].find('<')
            addr_end = data[1].find('>')
            from_addr = data[1][addr_start + 1 : addr_end]
            conn.sendall('250 Ok')

        elif data[0] == 'RCPT':
            addr_start = data[1].find('<')
            addr_end = data[1].find('>')
            from_addr = data[1][addr_start + 1 : addr_end]
            conn.sendall('250 Ok')

        elif data[0] == 'DATA':
            conn.sendall('354 End data with <CRLF>.<CRLF>')
            record = True
            while record:
                entry = conn.recv(1024)
                if entry == '.':
                    record = False
                    QUEUE += 1
                    conn.sendall('250 Ok: queued as ', QUEUE)
                else:
                    content.append(entry)
            
        elif data[0] == 'QUIT':
            conn.sendall('221 Bye')
            conn.close()
            connected = False

