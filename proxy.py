#!/usr/bin/python
import sys
import zmq
from zmq import Context

class Proxy:
    def __init__(self, address='*', port1='5566', port2='5567'):
        print("Current libzmq version is %s" % zmq.zmq_version())
        print("Current  pyzmq version is %s" % zmq.pyzmq_version())
        self.context = Context.instance()
        self.url1 = "tcp://{}:{}".format(address, port1)
        self.url2 = "tcp://{}:{}".format(address, port2)
        self.xpub_xsub_proxy()
    # N publishers to 1 sub <----> proxy 1 sub to 1 pub <----> publish to M subscribers
    def xpub_xsub_proxy(self):
        xsub = self.context.socket(zmq.XSUB)
        xsub.bind(self.url1)
        print("Subscribing %s"%self.url1)
        xpub = self.context.socket(zmq.XPUB)
        xpub.bind(self.url2)
        print("Publishing %s"%self.url2)
        poller = zmq.Poller()
        poller.register(xpub, zmq.POLLIN)
        poller.register(xsub, zmq.POLLIN)
        while True:
            events = dict(poller.poll(1000))
            if xpub in events:
                message = xpub.recv_multipart()
                print ("[BROKER] subscription message: %r" % message)
                xsub.send_multipart(message)
            if xsub in events:
                message = xsub.recv_multipart()
                print ("publishing message: %r" % message)
                xpub.send_multipart(message)
if __name__ == '__main__':
    print("Arguments given: {}".format(sys.argv))
    Proxy()