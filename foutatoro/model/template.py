#!/usr/bin/python
# Author: Alioune BA

class Template:

    def __init__(self, name=None, cpu=None, ram=None, disk=None):

        self.name = name
        self.cpu=cpu
        self.ram=ram
        self.disk=disk

    def get_name(self):
        return self.name

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_disk(self):
        return self.disk

    def __str__(self):
        print("Template name: %s, cpu %d, ram %d, disk %d" %(self.name, self.cpu, self.ram, self.disk))