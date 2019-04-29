import socket	#for sockets
import sys	#for exit
from thread import *

def create():
    #create an INET, STREAMing socket
    try:
	       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
	       print 'Failed to create socket'
	       sys.exit()
    print('Socket Created')
    return s

def bind(s, host, port):
    try:
    	s.bind((host, port))
    except socket.error , msg:
    	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    	sys.exit()
    print 'Socket bind complete'

def listen(s):
    s.listen(10)
    print 'Socket now listening'

def accept(s):
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	#infinite loop so that function do not terminate and thread do not end.
	while True:
		#Receiving from client
		data = conn.recv(1024)
		reply = 'OK...' + data
		if not data:
			break
		conn.sendall(reply)
	conn.close()

def startThreadedServer(s):
    while 1:
        #wait to accept a connection - blocking call
    	conn, addr = s.accept()
    	print 'Connected with ' + addr[0] + ':' + str(addr[1])
    	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    	start_new_thread(clientthread ,(conn,))

def getIp(host):
    try:
	remote_ip = socket.gethostbyname( host )

    except socket.gaierror:
	#could not resolve
	print 'Hostname could not be resolved. Exiting'
	sys.exit()
    return remote_ip

def connect(s, remote_ip, port):
    #Connect to remote server
    s.connect((remote_ip , port))
    print('Socket Connected to ' + str(remote_ip)  + ':' + str(port))

def send(s, message):
    try :
	#Set the whole string
	s.sendall(message)
    except socket.error:
	#Send failed
	print 'Send failed'
	sys.exit()
    print 'Message send successfully'

def receive(s):
    #Now receive data
    reply = s.recv(4096)
    print(reply)
    return reply

def close(s):
    print "Closing socket connection"
    s.close()
