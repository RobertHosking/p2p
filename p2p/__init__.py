import socket	#for sockets
import sys	#for exit
import os
from thread import *
import json
from requests import get
from helpers import *
import logging
logging.basicConfig(filename='p2p.log', filemode="a", format='%(asctime)s - %(message)s', level=logging.DEBUG)

messages = json.loads(open(os.path.join(os.path.dirname(__file__), 'messages.json')).read())

class Node:
    def __init__(self, port=8888 ):
        self.version = 1
        self.server = self.create('Inbound')
        self.client = self.create('Outbound')
        self.ip = self.getPublicIp()
        self.host = ''
        self.port = port
        self.peers = []

        print("Node is starting...")
        self.bind()
        self.listen()
        self.startServer()


    def create(self, label):
        #create an INET, STREAMing socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            logging.error(messages['socket']['create']['fail'].format(label))
            sys.exit()
        logging.info(messages['socket']['create']['win'].format(label))
        return s

    def bind(self):
        try:
        	self.server.bind((self.host, self.port))
        except socket.error , msg:
            logging.error(messages['socket']['bind']['fail'].format(str(msg[0]), msg[1]))
            sys.exit()
        logging.info(messages['socket']['bind']['win'])

    def listen(self):
        self.server.listen(10)
        logging.info(messages['socket']['listen']['win'].format(self.port))

    def package(self, type, message=''):
        return json.dumps({'type': type, 'message': message, 'ip': self.ip})

    def clientThread(self, conn):
    	#Sending message to connected client
    	#infinite loop so that function do not terminate and thread do not end.
    	while True:
    		#Receiving from client
            data = conn.recv(1024)
            if is_json(data):
                payload = json.loads(data)
                reply = self.respond(payload)
    		if not data:
    			break
    		conn.sendall(reply)
    	conn.close()

    def startThreadedServer(self):
        while 1:
            #wait to accept a connection - blocking call
            logging.debug("Waiting for connection")
            conn, addr = self.server.accept()
            logging.debug(conn + " " + addr)
            logging.info('Connected with ' + addr[0] + ':' + str(addr[1]))
            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(self.clientThread ,(conn,))

    def startServer(self):
        start_new_thread(self.startThreadedServer, ())

    def getPublicIp(self):
        try:
            ip = get('https://api.ipify.org').text
        except urllib.HTTPError, e:
            logging.error(messages['agent']['getPublicIp']['fail'].format(str(e.code)))
            sys.exit()
        logging.info(messages['agent']['getPublicIp']['win'].format(ip))
        return ip

    def getHostIp(self, host):
        try:
            remote_ip = socket.gethostbyname( host )
        except socket.gaierror:
        	logging.error(messages['agent']['getHostIp']['fail'].format(host))
        	sys.exit()
        logging.info(messages['agent']['getHostIp']['win'].format(host, remote_ip))
        return remote_ip

    def connect(self, remote_ip, port):
        #Connect to a new peer
        try:
            logging.info("Connecting to {0} on port {1}".format(remote_ip, port))
            self.client.connect((remote_ip , port))
        except socket.error, exc:
            logging.error(messages['socket']['connect']['fail'].format(exc))
            sys.exit()
        logging.info(messages['socket']['connect']['win'].format(remote_ip, str(port)))

    def send(self, package):
        try :
            self.client.sendall(package)
        except socket.error:
            logging.error(messages['socket']['send']['fail'])
            sys.exit()
        logging.info(messages['socket']['send']['win'])

    def respond(self, payload):
        '''
        for deciding what to do when I get a message
        '''
        type = payload['type']
        message = payload['message']
        ip = payload['ip']
        port = payload['port']
        if type == "ping":
            self.connect(ip, port)
            logging.info("Pinged by "+ip)
            return self.package('pong')
        elif type == "pong":
            self.peers.append(ip)
            logging.info("Peer {0} is active".format(message))
        elif type == "alert":
            logging.info(message)
            return self.package('ack', "Recieved: " + message)
        elif type == 'ack':
            logging.info(message)
            return
        else:
            return self.package('err', "Unknown message recieved")



    def close(s):
        logging.warning(messages['socket']['close'])
        s.close()
