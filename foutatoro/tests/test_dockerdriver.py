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


""" COMPUTE DOCKER TESTS"""

ip1 = IpAddres("net1","192.168.1.115")
ip2 = IpAddres("net2","192.168.2.125")
ip3 = IpAddres("net3","192.168.3.135")
list = []
list.append(ip2)
list.append(ip3)
compute = Compute("test-compute","ubuntu-ads",list)

docker_driver = ComputeDockerDriver()
docker_driver.delete_container(compute)
#docker_driver.create_docker_container(compute)


