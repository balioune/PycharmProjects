#!/usr/bin/python
import logging


class Network:

    counter=0
    logging.basicConfig(filename='myapp.log', level=logging.INFO)

    def __init__(self, name, address, mask):
        logging.info("Initializing a new network \n")
        self.net_name=name
        self.net_address=address
        self.net_mask=mask
        Network.counter+=1

    def __str__(self):
        print "Network information \n"
        print "Name: "+ self.net_name + "  Address: "+ self.net_address + "  Mask: "+ self.net_mask + "\n\n"

    def get_name(self):
        return self.net_name

#net1 = Network("net1", "192.168.1.0", "255.255.255.0")
#net1.__str__()
#print "counter: " + str(net1.counter)
#net1.type="traffic"

#net2 = Network("net2", "192.168.2.0", "255.255.255.0")
#net2.__str__()
#print "count: " + str(net2.counter)

