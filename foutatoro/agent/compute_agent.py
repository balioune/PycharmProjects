#!/usr/bin/env python
# Author: Alioune BA


from foutatoro.agent.kvm_driver import ComputeKvmDriver
from foutatoro.agent.docker_driver import ComputeDockerDriver

class ComputeAgent():

    def __init__(self):
        self.kvmdriver = ComputeKvmDriver()
        self.dockerdriver = ComputeDockerDriver()


    def create_compute_resoure(self,compute):
        response = 0
        if compute.get_compute_type().value == 1:
            response = self.kvmdriver.create_kvm_server(compute)

        elif compute.get_compute_type().value == 2:
            response = self.dockerdriver.create_docker_container(compute)

        return response


    def delete_compute_resource(self, compute):
        response=0
        if compute.get_compute_type().value == 1:
            response = self.kvmdriver.remove_kvm_server(compute)

        elif compute.get_compute_type().value == 2:
            response = self.dockerdriver.delete_container(compute)

        return response