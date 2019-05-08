from p2p import Node

a = Node(port=6666)
a.connect("localhost", 6667)
