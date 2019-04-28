from pyp2p.net import *
import time

#Setup Alice's p2p node.
def setup(ip, port, interface="eth0:2", node_type="passive", debug=1 ):
    alice = Net(passive_bind=ip, passive_port=port, interface=interface, node_type=node_type, debug=debug)
    alice.start()
    alice.bootstrap()
    alice.advertise()
    #Event loop.
    while 1:
        for con in alice:
            for reply in con:
                print(reply)
        time.sleep(1)

def joke():
    return ('Why\'d the chicken cross the road')
