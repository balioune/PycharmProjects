#!/usr/bin/python
# Author: Alioune BA
from __future__ import unicode_literals
from __future__ import print_function
import ipaddress



from foutatoro.model.network import Network
from foutatoro.model.network import NetworkType
from foutatoro.agent.network_agent import NetworkAgent


""" NETWORK TESTS"""

net1 = Network("net1", "192.168.1.0", NetworkType.MANAGEMENT,"eth1")
net2 = Network("net2", "192.168.2.0", NetworkType.MANAGEMENT,"eth0","255.255.0.0")
#net3 = Network("net3", "192.168.3.0", NetworkType.EXTERNAL,"eth12","255.0.0.0")
list = []
list.append(net1)
list.append(net2)
#list.append(net3)
agent = NetworkAgent()


agent.create_forwarding_graph(list)
#agent.delete_networks(list)
#print(ipaddress.IPv4Address("192.168.0.10")+5)
