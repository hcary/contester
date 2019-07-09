#!/usr/bin/env python

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
     
    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
         
    s.close()

def udp(HOST, PORT):
    '''
        udp socket client
        Silver Moon
    '''
    print "HOST: " + HOST
    # create dgram udp socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()
 
    while(1) :
        #msg = raw_input('Enter message to send : ')
        msg = "helo"
        print "Sending " + str(msg) + " to " + str(HOST) + ":" + str(PORT)
        try :
            #Set the whole string
            s.sendto(str(msg), (str(HOST), int(PORT)))
             
            # receive data from client (data, addr)
            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
             
            print 'Server reply : ' + reply
         
        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
            
def tcp(HOST, PORT):
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the port where the server is listening
    server_address = (HOST, PORT)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    
    try:
        
        # Send data
        message = 'This is the message.  It will be repeated.'
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)
    
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print >>sys.stderr, 'received "%s"' % data
    
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()

def print_options(proto, port, host):

    print 'Proto: ', proto
    print ' Port: ', port
    print ' Host: ', host

def main():

    parser = argparse.ArgumentParser(description='')

    parser.add_argument("-s", "--server", dest="server", action="store_true", default=False, help="Run in Server mode, default is client mode")
    parser.add_argument("-u", "--udp", dest="udp",  action="store_true", default=False, help="Protocol defaults to tcp")
    parser.add_argument("-p", "--port", dest="port",  action="store", type=int, default=80,  help="Default 80")
    parser.add_argument("-b", "--bind", dest="bind",  action="store", type=str, default="localhost",  help="Used in server mode, defaults to localhost")
    #parser.add_argument("host", action="store", help="Host to connect to used in client mode")
    #ma77h3wparser.add_argument('host', type=str, default="localhost", help='host')
    #parser.add_argument('string', metavar='N', type=int, nargs='+', help='an integer for the accumulator')


    args = parser.parse_args()

    #print args.positionals

    if args.server and args.udp:
        if args.udp:
            print_options("udp", args.port, args.bind)
            server_udp(args.bind, args.port)
        else:
            print_options("tcp", args.port, args.bind)
            server_tcp(args.bind, args.port)
    else:
        host = sys.argv[len(sys.argv) - 1]
        if args.udp:
            print_options("udp", args.port, host)
            tcp(args.host, args.port)
        else:
            print_options("tcp", args.port, host)
            tcp(args.host, args.port)



if __name__ == "__main__":
    main()