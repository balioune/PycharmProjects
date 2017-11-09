#!/usr/bin/python
# Author: Alioune BA

import logging
from enum import Enum

class ComputeType(Enum):
    """This declare all types of network in our system using enumeration"""
    KVM=1
    DOCKER=2

class IpAddres:
    def __init__(self,network,ip=None,mask="255.255.255.0"):
        self.net_name=network
        self.ip=ip
        self.mask=mask

    def get_net_name(self):
        return self.net_name

    def get_ip_address(self):
        return self.ip

    def get_mask(self):
        return self.mask

    def __str__(self):
        print ("net name "+ self.net_name)
        print ("IP address " + self.ip)
        print ("Mask "+ self.mask)

class Compute:

    def __init__(self, name, image=None, addresses=None, ram=None, cpu=None, type=ComputeType.KVM):
        self.name=name
        self.image=image
        self.addresses=addresses
        self.ram=ram  #converting ram from Megabyte to KiloByte in kvmdriver
        self.cpu=cpu
        self.type=type


    def get_compute_name(self):
        return  self.name

    def get_compute_image(self):
        return self.image

    def get_compute_ipaddresses(self):
        return self.addresses

    def get_compute_ram(self):
        return self.ram

    def get_compute_cpu(self):
        return self.cpu

    def get_compute_type(self):
        return self.type