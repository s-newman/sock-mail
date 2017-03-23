# Sean Newman
import socket

def send_print(sock, data, server=False):
    sock.sendall(data)
    if server:
        print 'SERVER: ' + data
    else:
        print 'CLIENT: ' + data

def recv_print(sock, server=False):
    data = sock.recv(1024)
    if server:
        print 'CLIENT: ' + data
    else:
        print 'SERVER: ' + data

def send_recv(sock, data, server=False):
    send_print(sock, data, server)
    recv_print(sock, server)

