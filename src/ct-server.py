#!/usr/bin/python

import sys
import socket
import getopt
 

proto = 'TCP'
PORT = 8080
HOST = 'localhost'                       # Symbolic name meaning all available interfaces

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

try:
    opts, args = getopt.getopt(sys.argv[1:],"hup:",["port=", "host="])
except getopt.GetoptError:
    print 'sys.argv[0] '
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print sys.argv[0] + ' -p <port> -u'
        sys.exit()
    elif opt in ("-u", "--udp"):
        proto = "UDP"
    elif opt in ("-p", "--port"):
        PORT = int(arg)
    elif opt in ("--host"):
        HOST = arg      

print 'Proto: ', proto
print ' Port: ', PORT
print ' Host: ', HOST

if proto == "UDP":
    server_udp(HOST, PORT)
else:
    server_tcp(HOST, PORT)
