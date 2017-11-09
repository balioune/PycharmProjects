#!/usr/bin/python
# Copyright 2017 Airbus Defence and Space
# Author: Alioune BA
import subprocess

output=subprocess.check_output(["sudo", "ovs-vsctl", "show"])

print ("printing the output")
print (output)