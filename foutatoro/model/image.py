#!/usr/bin/python
# Author: Alioune BA

class Image:

    def __init__(self, name, type, nfvi=None):

        self.name=name
        self.type=type
        self.nfvi=nfvi


    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_nfvi(self):
        return self.nfvi
