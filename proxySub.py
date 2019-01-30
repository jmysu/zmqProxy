#!/usr/bin/python
import sys
import zmq
from zmq import Context
import time
import socket

class ProxySub:
    def __init__(self, address='127.0.0.1', port='5567'):
        print("Current libzmq version is %s" % zmq.zmq_version())
        print("Current  pyzmq version is %s" % zmq.pyzmq_version())
        if len(sys.argv) > 1:
            address =  sys.argv[1]
        if len(sys.argv) > 2:
            port = sys.argv[2]
        self.context = Context.instance()
        self.url = "tcp://{}:{}".format(address, port)
        self.hostname = socket.gethostname()
        self.sub_ep_time()

    def sub_ep_time(self):
        sub = self.context.socket(zmq.SUB)
        sub.connect(self.url)
        sub.setsockopt(zmq.SUBSCRIBE, b"")
        #sub.setsockopt(zmq.SUBSCRIBE, self.hostname)
        while True:
            msg_received = sub.recv_multipart()
            print("sub : {}".format(msg_received))

if __name__ == '__main__':
    ProxySub()