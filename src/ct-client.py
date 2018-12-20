#!/usr/bin/python

import sys
import socket
import getopt
 

proto   = 'TCP'
HOST    = 'localhost'
PORT    = 8080
VERBOSE = 0

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
        

try:
    opts, args = getopt.getopt(sys.argv[1:],"hup:",["port=", "host="])
except getopt.GetoptError:
    print 'test.py -i <inputfile> -o <outputfile>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'ct-server -p <port> -u'
        sys.exit()
    elif opt in ("-u", "--udp"):
        proto = "UDP"
    elif opt in ("-p", "--port"):
        PORT = int(arg)
    elif opt in ("--host"):
        HOST = arg
    elif opt in ("-v"):
        VERBOSE = 1 

print 'Proto: ', proto
print ' Port: ', PORT
print ' Host: ', HOST

if proto == "UDP":
    udp(HOST, PORT)
else:
    tcp(HOST, PORT)
