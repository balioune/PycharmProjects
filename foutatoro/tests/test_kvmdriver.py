#!/usr/bin/python
# Author: Alioune BA
from __future__ import print_function
import sys
import libvirt
import subprocess

from foutatoro.model.compute import ComputeType
from foutatoro.model.compute import Compute
from foutatoro.model.compute import IpAddres


from foutatoro.model.network import Network
from foutatoro.model.network import NetworkType

from foutatoro.agent.docker_driver import ComputeDockerDriver
from foutatoro.agent.kvm_driver import ComputeKvmDriver


""" REAL COMPUTE KVM TESTS"""

""" Creating IP address"""
addr1 = IpAddres("net1","192.168.1.15")
addr2 = IpAddres("net2","192.168.2.25")
addr3 = IpAddres("net3","192.168.3.35")

addr_list = []
addr_list.append(addr1)
addr_list.append(addr2)
addr_list.append(addr3)


""" Creating compute type"""
compute1 = Compute("router","ubuntu-14.04-server-cloudimg-amd64-disk1.img",addr_list,1024,1)

kvmdriver=ComputeKvmDriver()

#kvmdriver.create_kvm_server(compute1)

kvmdriver.remove_kvm_server(compute1)