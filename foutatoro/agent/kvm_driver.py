#!/usr/bin/python
# Author: Alioune BA

from __future__ import print_function
import sys, time
import libvirt
from xml.dom import minidom
import subprocess

from foutatoro.model.compute import ComputeType
from foutatoro.model.compute import Compute

from foutatoro.model.network import NetworkType
from foutatoro.model.network import Network


class ComputeKvmDriver:

    def __init__(self):

        self.connection = libvirt.open('qemu:///system')
        if self.connection == None:
            print('Failed to open connection to qemu:///system', file=sys.stderr)
            exit(1)

    def generate_net_xml(self, ipaddress):
        return "<interface type='network'> \
                  <source network='" + ipaddress.get_net_name() + "'/> \
                </interface> " \


    """ Generate userdata for adding passwork and/or packages/commands to run when the VM is UP"""
    """ Prebuild image with confd to connect to the SDN controller"""
    def create_userdata(self):
        userdata="#cloud-config \n password: password \n chpasswd: {expire: False} \n ssh_pwauth: True"

        domain_file = open("../files/user-data", "w+")
        domain_file.write(userdata)
        domain_file.close()

    """ Generate metadata to set up addresses of VM in each network"""
    def create_medata(self,vnf_name,addresses):

        metadata="instance-id: iid-"+vnf_name+";"\
                 "\nnetwork-interfaces: |"

        index_if=0

        for address in addresses:
            metadata = metadata + \
                       "\n  auto eth"+str(index_if) + \
                       "\n  iface eth"+str(index_if)+ " inet static " + \
                       "\n  address "+ address.get_ip_address() + \
                       "\n  netmask "+ address.get_mask()

            index_if = index_if+1

        metadata = metadata +"\nhostname: " + vnf_name + \
        "\nlocal-hostname: " + vnf_name

        domain_file = open("../files/meta-data", "w+")
        domain_file.write(metadata)
        domain_file.close()
        return 1


    def create_domain_image_disk(self,vnf_name,image):
        subprocess.check_output(["sudo", "virsh", "vol-clone", "--pool", "nfv", image, vnf_name + ".img"])
        return 1

    def create_domain_iso_disk(self,vnf_name):
        subprocess.check_output(["sudo", "genisoimage", "-output", vnf_name+".iso","-volid", "cidata", "-joliet", "-rock", "../files/user-data", "../files/meta-data"])
        subprocess.check_output(["sudo", "mv", vnf_name+".iso", "/home/nfv"])
        subprocess.check_output(["sudo", "virsh", "pool-refresh", "nfv"])
        return 1


    """Generate XML domain definition file"""
    def get_xml_dom(self,name,ram,cpu,ipaddresses):

        iso_file="/home/nfv/"+name+".iso"
        image_file = "/home/nfv/" + name + ".img"
        net_xml=""
        ram_KB = ram*1000

        for ipaddress in ipaddresses:
            net_xml=net_xml+ self.generate_net_xml(ipaddress)

        return "<domain type=\'kvm\'> \
          <name>"+name+ "</name> \
          <memory>"+str(ram_KB)+"</memory> \
          <currentMemory>"+str(ram_KB)+"</currentMemory> \
          <vcpu>"+str(cpu)+"</vcpu> \
          <os> \
            <type arch='x86_64' machine='pc'>hvm</type> \
            <boot dev='hd'/> \
          </os> \
          <features> \
            <acpi/> \
            <apic/> \
            <pae/> \
          </features> \
          <clock offset='utc'/> \
          <on_poweroff>destroy</on_poweroff> \
          <on_reboot>restart</on_reboot> \
          <on_crash>restart</on_crash> \
          <devices> \
            <emulator>/usr/bin/kvm-spice</emulator> \
            <disk type='file' device='disk'> \
              <driver name='qemu' type='qcow2'/> \
              <source file='"+image_file+"'/> \
              <target dev='vda'  bus='virtio'/> \
            </disk> \
            <disk type='file' device='disk'> \
               <driver name='qemu' type='raw'/> \
               <source file='"+iso_file+"'/> \
               <target dev='vdb'  bus='virtio'/> \
            </disk>"+ \
            net_xml \
            +"<graphics type='vnc' port='-1'/> \
            <serial type='pty'> \
               <target port='0' /> \
            </serial> \
            <console type='pty'> \
               <target type='serial' port='0' /> \
            </console > \
        </devices> \
        </domain>"


    """ Creating KVM compute"""
    def create_kvm_server(self, compute):

        # generating xml config for the compute
        xmlconfig = self.get_xml_dom(compute.get_compute_name(), compute.get_compute_ram(),
                                          compute.get_compute_cpu(), compute.get_compute_ipaddresses())

        # creating metadata file
        self.create_medata(compute.get_compute_name(), compute.get_compute_ipaddresses())

        # creating userdata file
        self.create_userdata()

        # creating iso file
        self.create_domain_iso_disk(compute.get_compute_name())

        # creating image disk
        self.create_domain_image_disk(compute.get_compute_name(),compute.get_compute_image())

        # creating the domain from the generated xml
        domaim = self.connection.createXML(xmlconfig, 0)
        if domaim == None:
            print('Failed to create a domain from an XML definition.', file=sys.stderr)
            exit(1)


        print('Guest ' + domaim.name() + ' has booted', file=sys.stderr)

        return 1


    def remove_kvm_server(self,compute):
        subprocess.check_output(["sudo", "virsh", "destroy", compute.get_compute_name()])

        # removing KVM disks
        subprocess.check_output(["sudo", "rm", "/home/nfv/"+compute.get_compute_name()+".iso"])
        subprocess.check_output(["sudo", "rm", "/home/nfv/" + compute.get_compute_name() + ".img"])
        subprocess.check_output(["sudo", "virsh", "pool-refresh", "nfv"])

        return 1