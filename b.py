from p2p import Node
from thread import *


b = Node(port=6666)
b.startThreadedServer()
# client = p2p.create()
#
# host = p2p.getIp('www.google.com');
# port = 80;
#
# p2p.connect(client, host, port)
#
# p2p.send(client, "GET / HTTP/1.1\r\n\r\n")
# p2p.receive(client)
#
# HOST = ''	# Symbolic name meaning all available interfaces
# PORT = 8888	# Arbitrary non-privileged port
#
# server = p2p.create()
# p2p.bind(server, HOST, PORT)
# p2p.listen(server)
# p2p.startThreadedServer(server)
