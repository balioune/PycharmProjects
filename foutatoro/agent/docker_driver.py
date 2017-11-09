#!/usr/bin/python
# Author: Alioune BA

from __future__ import print_function
from docker import Client
from pyroute2 import IPRoute
from pyroute2 import netns

import subprocess

class ComputeDockerDriver:

    def __init__(self):
        self.client = Client(base_url='unix://var/run/docker.sock')
        self.ip = IPRoute()


    def create_docker_container(self,compute):

        print ("Creating container "+ compute.get_compute_name())
        self.client.create_container(name=compute.get_compute_name(),image=compute.get_compute_image(),detach=True, tty=True,network_disabled=True)
        self.client.start(compute.get_compute_name())
        id_veth = 0

        """Getting required information of the create container """

        inspect = self.client.inspect_container(compute.get_compute_name())
        PID = inspect['State']['Pid']
        proc_pid = "/proc/" + str(PID) + "/ns/net"
        var_run_pid = "/var/run/netns/" + str(PID)
        subprocess.check_output(["sudo", "ln", "-s", proc_pid, var_run_pid])

        """Create veth interfaces and attach them to the appropriate networks"""

        for ipaddress in compute.get_compute_ipaddresses():

            """Create veth pairs. veth1: virtual link (vl) attached to the OVS bridge and veth2 moved to the namespace"""

            veth1='vl-'+str(id_veth)+'-'+str(PID)
            veth2='if-'+str(id_veth)+'-'+str(PID)

            self.ip.link("add", ifname=veth1, peer=veth2, kind="veth")
            """Set veth links to up """
            self.ip.link_lookup(ifname=veth1)[0]
            idx=self.ip.link_lookup(ifname=veth2)[0]

            """ Set veth2 to the namespace of the container"""

            self.ip.link('set',index=idx,net_ns_fd=str(PID))

            """Add the veth1 to the OpenvSwitch bridge"""

            subprocess.check_output(["sudo", "ovs-vsctl", "add-port", "br-" +ipaddress.get_net_name(), veth1])

            """Assign the appropriate IP address on each interface"""
            subprocess.check_output(["sudo", "ip", "netns", "exec", str(PID), "ifconfig",veth2,"up"])
            subprocess.check_output(["sudo", "ip", "netns", "exec", str(PID), "ifconfig", veth2, ipaddress.get_ip_address(), "netmask", ipaddress.get_mask()])

            id_veth=id_veth+1

        print("The container " + compute.get_compute_name() + " is created ")
        return 1


    def delete_container(self,compute):

        inspect = self.client.inspect_container(compute.get_compute_name())
        PID = inspect['State']['Pid']
        self.client.stop(compute.get_compute_name())
        self.client.remove_container(compute.get_compute_name())
        netns.remove(str(PID))

        id_veth=0

        """Remove veth interfaces to OpenvSwitch bridges"""

        for ipaddress in compute.get_compute_ipaddresses():
            veth1='vl-'+str(id_veth)+'-'+str(PID)
            subprocess.check_output(["sudo", "ovs-vsctl", "del-port", "br-" + ipaddress.get_net_name(), veth1])
            id_veth = id_veth + 1
        return 1