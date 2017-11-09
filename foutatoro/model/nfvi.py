#!/usr/bin/python
# Author: Alioune BA

class Nfvi:

    def __init__(self, id, hostname, cpu=None, ram=None, disk=None):

        self.id=id
        self.hostname=hostname
        self.cpu=cpu
        self.ram=ram
        self.disk=disk

    def get_id(self):
        return self.id

    def get_hostname(self):
        return self.hostname

    def get_cpu(self):
        return self.cpu

    def get_ram(self):
        return self.ram

    def get_disk(self):
        return self.disk
