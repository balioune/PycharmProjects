#!/usr/bin/python
# Author: Alioune BA
import logging
from enum import Enum

class NetworkType(Enum):
    """This declare all types of network in our system using enumeration"""
    TRAFFIC=1
    EXTERNAL=2
    MANAGEMENT=3


class Network:
    """This class defines a model of network.
    It will implement all kinds of network instantiation
    and all required methods and attributes"""

    def __init__(self, name, address=None, type=None, nic=None, subnet='255.255.255.0', nfvi=None):
        logging.info("Initializing a new network")
        logging.basicConfig(filename='logs/networks.log', level=logging.INFO)
        self.name=name
        self.address=address
        self.subnet=subnet
        self.type=type
        self.nic=nic
        self.nfvi=nfvi

    def get_name(self):
        return self.name

    def get_network(self):
        return self.address

    def get_subnet(self):
        return self.subnet

    def get_type(self):
        return self.type

    def get_nic(self):
        return self.nic

    def get_nfvi(self):
        return self.nfvi

    def __str__(self):
        print("Network name: %s, address %s, subnet %s " %(self.name, self.network, self.subnet) )