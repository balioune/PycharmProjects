#!/usr/bin/python
# Author: Alioune BA

from __future__ import unicode_literals
from __future__ import print_function
import sys
import libvirt
import subprocess
import netifaces
import ipaddress

from foutatoro.model.network import Network
from foutatoro.model.network import NetworkType

class NetworkAgent:

    def __init__(self):

        self.connection = libvirt.open('qemu:///system')
        if self.connection == None:
            print('Failed to open connection to qemu:///system', file=sys.stderr)
            exit(1)

    """Create an OVS bridge"""
    def create_ovs_bridge(self,name):

        print("Creating OVS bridge "+name)
        subprocess.check_output(["sudo", "ovs-vsctl", "add-br", "br-" + name])

    """Get xml defining the network"""
    def get_network_xlm(self,name):

        xml=bridge_name="br-"+name

        return "<network> \
        <name>"+name +"</name> \
        <forward mode='bridge'/> \
        <bridge name="+"\'"+bridge_name+"\'"+"/> \
        <virtualport type='openvswitch'>  </virtualport > \
        </network > "

    def create_forwarding_graph(self,networks):

        # Creating networks composing the forwarding graph
        created_networks = []

        for network in networks:

            net_xml=self.get_network_xlm(network.get_name())

            self.create_ovs_bridge(network.get_name())

            # creating a persistent virtual network
            net = self.connection.networkCreateXML(net_xml)

            if net == None:

                print('Failed to create a virtual network', file=sys.stderr)
                exit(1)

            active = net.isActive()

            if active == 1:

                print('The new persistent virtual network is active')
                created_networks.append(network)
            else:
                print('The new persistent virtual network is not active')

            if network.get_type().value==3:
                print ("Network type is MANAGEMENT")
                bridge_ip=ipaddress.IPv4Address(network.get_network())+1
                print ("printing bridge IP")
                print(bridge_ip)
                subprocess.check_output(["sudo", "ifconfig", "br-" + network.get_name(), str(bridge_ip),"netmask" ,network.get_subnet(), "up"])

            if network.get_type().value==2:
                print("Network type is EXTERNAL")
                if network.get_nic() in netifaces.interfaces():

                    subprocess.check_output(["sudo", "ovs-vsctl", "add-port", "br-" + network.get_name(), network.get_nic()])
                else:
                    print ("No interface has name "+ network.get_nic())
                    self.delete_networks(created_networks)
                    #exit(1)

            if network.get_type == NetworkType.TRAFFIC:
                print("Network type is TRAFFIC")
   
        return 1

    def delete_networks(self,networks):

        for network in networks:

            # now destroy the persistent virtual network
            net = self.connection.networkLookupByName(network.get_name())
            print("Deleting "+network.get_name())
            #net.destroy()
            subprocess.check_output(["sudo", "virsh", "net-destroy", network.get_name()])
            subprocess.check_output(["sudo", "ovs-vsctl", "del-br", "br-" + network.get_name()])

        return 1

    def delete_network(self,name):

        # now destroy the persistent virtual network
        net = self.connection.networkLookupByName(name)
        print("Deleting " + name)
        # net.destroy()
        subprocess.check_output(["sudo", "virsh", "net-destroy", name])
        subprocess.check_output(["sudo", "ovs-vsctl", "del-br", "br-" + name])

        return 1