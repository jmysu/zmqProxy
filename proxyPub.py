#!/usr/bin/python
import sys
import zmq
from zmq import Context
import time
import socket  

class ProxyPub:
    def __init__(self, address='127.0.0.1', port='5566'):
        print("Current libzmq version is %s" % zmq.zmq_version())
        print("Current  pyzmq version is %s" % zmq.pyzmq_version())
        if len(sys.argv) > 1:
            address =  sys.argv[1]
        if len(sys.argv) > 2:
            port = sys.argv[2]
        self.context = Context.instance()
        self.url = "tcp://{}:{}".format(address, port)
        self.hostname = socket.gethostname()
        self.pub_ep_time()

    def pub_ep_time(self):
        pub = self.context.socket(zmq.PUB)
        pub.connect(self.url)
        print("Publishing to %s"%self.url)
        while True:
            pub.send_multipart([self.hostname, time.strftime("%H:%M:%S")])
            print("Pub {}: '{}' ".format(self.hostname, time.strftime("%H:%M:%S")))
            time.sleep(1)

if __name__ == '__main__':
    ProxyPub()