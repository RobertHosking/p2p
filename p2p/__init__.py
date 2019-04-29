import socket	#for sockets
import sys	#for exit
import os
from thread import *
import json
from requests import get

messages = json.loads(open(os.path.join(os.path.dirname(__file__), 'messages.json')).read())

class Node:
    def __init__(self, port=8888, ):
        self.client = self.create('Outbound')
        self.server = self.create('Inbound')
        self.ip = ''
        self.host = ''
        self.port = port
        self.peers = []

        self.getPublicIp()
        self.bind()
        self.listen()
        self.startThreadedServer()

    def create(self, label):
        #create an INET, STREAMing socket
        try:
    	       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
    	       print(messages['socket']['create']['fail'].format(label))
    	       sys.exit()
        print(messages['socket']['create']['win'].format(label))
        return s

    def bind(self):
        try:
        	self.server.bind((self.host, self.port))
        except socket.error , msg:
        	print(messages['socket']['bind']['fail'].format(str(msg[0]), msg[1]))
        	sys.exit()
        print(messages['socket']['bind']['win'])

    def listen(self):
        self.server.listen(10)
        print(messages['socket']['listen']['win'])

    def clientthread(self, conn):
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

    def startThreadedServer(self):
        while 1:
            #wait to accept a connection - blocking call
        	conn, addr = self.server.accept()
        	print 'Connected with ' + addr[0] + ':' + str(addr[1])
        	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        	start_new_thread(self.clientthread ,(conn,))

    def getPublicIp(self):
        try:
            ip = get('https://api.ipify.org').text
        except urllib.HTTPError, e:
            print(messages['agent']['getPublicIp']['fail'].format(str(e.code)))
        print(messages['agent']['getPublicIp']['win'].format(ip))
        self.ip = ip

    def getHostIp(self, host):
        try:
    	    remote_ip = socket.gethostbyname( host )
        except socket.gaierror:
        	print(messages['agent']['getHostIp']['fail'].format(host))
        	sys.exit()
        print(messages['agent']['getHostIp']['win'].format(host, remote_ip))
        return remote_ip

    def connect(s, remote_ip, port):
        #Connect to a new peer
        try:
            s.connect((remote_ip , port))
        except socket.error, exc:
            print(messages['socket']['connect']['fail'].format(exc))
        print(messages['socket']['connect']['win'].format(remote_ip, str(port)))

    def send(s, message):
        try :
        	#Set the whole string
        	s.sendall(message)
        except socket.error:
        	#Send failed
        	print messages['socket']['send']['fail']
    	sys.exit()
        print(messages['socket']['send']['win'])

    def close(s):
        print(messages['socket']['close'])
        s.close()
