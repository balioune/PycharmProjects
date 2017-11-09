#!/usr/bin/env python

from docker import Client
import docker
from pyroute2 import IPRoute
from pyroute2 import netns
import subprocess

"""
client = docker.from_env()
## create container
client.containers.create("ubuntu:latest",name="container-python", detach=True, tty=True)
id_container = client.containers.get("container-python")
#subprocess.Popen(["sudo", "docker", "rm", "container-python"],stdout=subprocess.PIPE)
container = client.containers.get("container-python")
PID=container.attrs['State']['Pid']
print ("Printing PID: ")
print PID
print "Printing container's ID"
print id_container
"""

"""
cmd = docker.from_env()
id_container = cmd.containers.get("python-container")
print ("Printing ID container ")
print id_container
"""

##http://containertutorials.com/py/docker-py.html

client = Client(base_url='unix://var/run/docker.sock')

#Stop and remove
#client.stop("python-container")
#client.remove_container("python-container")

# create and start the container
client.create_container(name="python-container",image="ubuntu:latest", detach=True, tty=True)
client.start("python-container")

# Get the PID
container =  client.containers(filters={"name": "python-container"})
inspect = client.inspect_container("python-container")
PID=inspect['State']['Pid']
print ("Printing PID: ")
print PID

print ("Move the namespace to /var/run/netns/")

proc_pid="/proc/"+str(PID)+"/ns/net"
var_run_pid="/var/run/netns/"+str(PID)
print proc_pid
print var_run_pid
subprocess.Popen(["sudo", "ln", "-s", proc_pid,var_run_pid], stdout=subprocess.PIPE)

client.stop("python-container")
client.remove_container("python-container")
netns.remove(str(PID))

## remove namespace associated to the namespace
#netns.remove('test')

# Create veth pair
ip = IPRoute()

#ip.link('del', ifname='v0p1')
#ip.link('add', ifname='v0p0', peer='v0p1', kind='veth')
#idx = ip.link_lookup(ifname='v0p1')[0]
#idx = ip.link_lookup(ifname='v0p0')[0]

#netns.remove('test')
#netns.create('test')