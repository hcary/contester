#!/usr/bin/env python3

from __future__ import absolute_import
import sys
import socket
import argparse


def server_udp(HOST, PORT):

    # Datagram (udp) socket
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, msg :
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket created'     
     
    # Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error, msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
         
    print 'Socket bind complete'
     
    #now keep talking with the client
    while 1:
        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]
         
        if not data: 
            break
         
    reply = 'OK...' + data
     
    s.sendto(reply , addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
     
    s.close()

def server_tcp(HOST, PORT):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
     
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
         
    print 'Socket bind complete'
     
    #Start listening on socket
    s.listen(10)
    print 'Socket now listening'
    print '================================================='
     
    #now keep talking with the client
    while True:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])

    s.close()

def print_options(proto, port, host):

    print 'Proto: ', proto
    print ' Port: ', port
    print ' Host: ', host

def main():

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-s', '--server', dest='server', action='store_true', default=False, help='Run in Server mode, default is client mode')
    parser.add_argument('-u', '--udp', dest='udp',  action='store_true', default=False, help='Protocol defaults to tcp')
    parser.add_argument('-p', '--port', dest='port',  action='store', type=int, default=80,  help='Default 80')
    parser.add_argument('-b', '--bind', dest='bind',  action='store', type=str, default='localhost',  help='Used in server mode, defaults to localhost')
    #parser.add_argument('host', action='store', help='Host to connect to used in client mode')

    args = parser.parse_args()

    if args.udp:
        print_options('udp', args.port, args.bind)
        server_udp(args.bind, args.port)
    else:
        print_options('tcp', args.port, args.bind)
        server_tcp(args.bind, args.port)


if __name__ == '__main__':
    main()