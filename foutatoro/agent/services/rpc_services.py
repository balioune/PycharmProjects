#!/usr/bin/env python
# Author: Alioune BA

import pika
import ConfigParser
import json

from foutatoro.model.network import Network
from foutatoro.model.network import NetworkType
from foutatoro.agent.network_agent import NetworkAgent
from foutatoro.model.compute import Compute
from foutatoro.agent.compute_agent import ComputeAgent
from foutatoro.model.compute import ComputeType
from foutatoro.model.compute import IpAddres


class RpcServices:

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('../config/nfvi_configs.cfg')
        self.rabbit_server = self.config.get('rabbitmq','rabbitmq_server')
        self.nfvi_id = self.config.get('nfvi','nfvi_id')

        """Init connection to rabbitmq server"""
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbit_server))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='nfvi.'+self.nfvi_id)

        self.network_agent = NetworkAgent()
        self.compute_agent = ComputeAgent()

    def on_request(self,ch, method, props, body):

        response = json.loads('{ "message": "ERROR"}')

        """ Parsing the received message """
        parsed_json = json.loads(body)
        key_list = parsed_json.keys()
        # get the type of the message from the VIM and then execute required tasks
        message_type = key_list[0]
        print ("Printing the message type: "+message_type)

        networks_list = []
        computes_list = []

        return_net=0
        return_compute=0

        if message_type == "service":
            print("creating a new service")
            print (parsed_json['service']['service_function_forwarder'])

            """ Get JSON Forwrding Graphs and instantiate Networks objects"""
            for iter_networks in range(len(parsed_json['service']['service_function_forwarder'])):

                network=parsed_json['service']['service_function_forwarder'][iter_networks]

                if network['type']=="MANAGEMENT" or network['type']=="TRAFFIC":

                    if 'subnet'in network:

                        networks_list.append(Network(network['name'], network['address'], NetworkType.MANAGEMENT, network['subnet']))

                    else:

                        networks_list.append(Network(network['name'], network['address'], NetworkType.MANAGEMENT))

                elif network['type']=="EXTERNAL":

                    if 'subnet'in network:

                        networks_list.append(Network(network['name'], network['address'], NetworkType.MANAGEMENT, network['subnet']))

                    else:

                        networks_list.append(Network(network['name'], network['address'], NetworkType.MANAGEMENT))


            """ Get JSON Computes and instantiate Compute objects"""

            for iter_computes in range(len(parsed_json['service']['computes'])):

                compute=parsed_json['service']['computes'][iter_computes]

                """ Get Address IPs of the compute """
                addr_list = []

                for iter_ips in range(len(compute['networks'])):

                    ip = compute['networks'][iter_ips]
                    if 'mask' in ip:
                        addr_list.append(IpAddres(ip['name'], ip['ip-address'], ip['mask']))
                    else:
                        addr_list.append(IpAddres(ip['name'], ip['ip-address']))

                if compute['type'] == "KVM":

                    computes_list.append(Compute(compute['name'], compute['image'], addr_list, int(compute['ram']), int(compute['cpu'])))

                elif compute['type'] == "DOCKER":
                    computes_list.append(
                        Compute(compute['name'], compute['image'], addr_list, type=ComputeType.DOCKER))


            """ Creating Networks of the Forwarding Graph"""
            return_net = self.network_agent.create_forwarding_graph(networks_list)

            """ Create computes in computes_list"""
            for compute in computes_list:
                return_compute=self.compute_agent.create_compute_resoure(compute)

            if return_net==1 and return_compute==1:
                response['message']="Service Created"

        elif message_type == "delete":

            print("Deleting a network service")
            print (parsed_json['delete']['computes'])

            """ GET all computes to delete"""
            for iter_computes in range(len(parsed_json['delete']['computes'])):

                addr_list = []

                compute=parsed_json['delete']['computes'][iter_computes]

                """ Check the type of compute"""
                if compute['type'] == "KVM":

                    computes_list.append(Compute(compute['name'], type=ComputeType.KVM))

                elif compute['type'] == "DOCKER":
                    for iter_ips in range(len(compute['networks'])):
                        ip = compute['networks'][iter_ips]
                        addr_list.append(IpAddres(ip['name']))
                    computes_list.append(Compute(compute['name'], addresses=addr_list, type=ComputeType.DOCKER))



            """ GET all networks to delete"""
            for iter_networks in range(len(parsed_json['delete']['service_function_forwarder'])):

                network = parsed_json['delete']['service_function_forwarder'][iter_networks]

                networks_list.append(Network(network['name']))
                #self.network_agent.delete_network(network['name'])

            """ Delete computes in computes_list"""
            for compute in computes_list:
                return_compute=self.compute_agent.delete_compute_resource(compute)

            """ Deleting Networks"""
            return_net=self.network_agent.delete_networks(networks_list)

            if return_net==1 and return_compute==1:
                response['message']="Service Deleted"



        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def start_rpc_service(self):

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue='nfvi.'+self.nfvi_id)
        print("Awaiting RPC requests from the VIM")
        self.channel.start_consuming()