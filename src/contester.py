#!/usr/bin/python

import sys
import socket
import getopt
from optparse import OptionParser


#
# Class to support tcp and udp server

def server_udp(bind, port):

    # Datagram (udp) socket
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, msg :
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket created'     
     
    # Bind socket to local host and port
    try:
        srv.bind((bind, port))
    except socket.error, msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
         
    print 'Socket bind complete'
     
    #now keep talking with the client
    while 1:
        # receive data from client (data, addr)
        d = srv.recvfrom(1024)
        data = d[0]
        addr = d[1]
         
        if not data: 
            break
         
    reply = 'OK...' + data
     
    srv.sendto(reply , addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
     
    srv.close()

def server_tcp(bind, port):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the port
    server_address = (bind, port)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    
    # Listen for incoming connections
    sock.listen(1)
    
    while True:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
    
        try:
            print >>sys.stderr, 'connection from', client_address
    
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                print >>sys.stderr, 'received "%s"' % data
                if data:
                    print >>sys.stderr, 'sending data back to the client'
                    connection.sendall(data)
                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
                
        finally:
            # Clean up the connection
            connection.close()

class client:

    def __init__(self, host, port):
        
        self.host = host
        self.port = int(port)

    def udp():
        '''
            udp socket client
            Silver Moon
        '''
        print "HOST: " + host
        # create dgram udp socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
     
        while(1) :
            #msg = raw_input('Enter message to send : ')
            msg = "helo"
            print "Sending " + str(msg) + " to " + str(host) + ":" + str(port)
            try :
                #Set the whole string
                srv.sendto(str(msg), (str(host), int(port)))
                 
                # receive data from client (data, addr)
                d = srv.recvfrom(1024)
                reply = d[0]
                addr = d[1]
                 
                print 'Server reply : ' + reply
             
            except socket.error, msg:
                print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                sys.exit()
                
    def tcp(self):
        
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print type(self.host)
        print type(self.port)
        
        #port = 443
        # Connect the socket to the port where the server is listening
        server_address = (self.host, self.port)
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
        

parser = OptionParser("usage: %prog [options] ",
    version="%prog 1.0")

parser.add_option("-s", "--server",
    action="store_true",
    dest="server",
    default=False)


parser.add_option("-u", "--udp",
    action="store_true",
    dest="proto_udp",
    default=False)

parser.add_option("-p", "--port",
    action="store",
    type="string",
    dest="port",
    default='8080',
    help="Set the Port")


#parser.add_option("-h", "--host",
#    action="store",
#    type="string",
#    dest="host",
#    help="")

parser.add_option("-b", "--bind",
    action="store",
    type="string",
    dest="bind",
    default='localhost',
    help="")


(options, args) = parser.parse_args()

arg_count = len(sys.argv)

bind = options.bind
port = int(options.port)

if options.server:
    
    if options.proto_udp:
        server_udp(bind, port)
    else:
        server_tcp(bind, port)
 
else:
    
    
    host = sys.argv[arg_count - 1]
    print "Host: " + host
    
    c = client(host, port)
    
    if options.proto_udp:
        #client_udp(host, port)
        c.udp
    else:
        #client_tcp(host, port)
        c.tcp()


