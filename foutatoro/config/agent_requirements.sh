#!/bin/bash

# Author: Alioune BA
# Configure the NFVI to use nfv pool in /home/nfv

sudo apt-get update
sudo apt-get install python-pip -y
sudo apt-get install genisoimage -y

sudo pip install netifaces
sudo pip install libvirt
sudo pip install pyroute2

#sudo pip install psutil
#sudo pip install blinkstick

# init "/proc/ns/net"
sudo ip netns add test
sudi ip netns delete test