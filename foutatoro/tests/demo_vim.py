#!/usr/bin/env python
# Author: Alioune BA

import pika
import uuid
import json


service1="""
{
   "service":{
      "network_service_type": "manpack", 
      "service_function_forwarder":
      [
         {
             "name": "net1", 
             "address":"192.168.1.0",
             "mask": "255.255.255.0",
             "type":"TRAFFIC"
         },
         {
             "name": "net2", 
             "address":"192.168.2.0",
             "mask": "255.255.255.0",
             "type":"TRAFFIC"
         },
         {
             "name": "net3", 
             "address":"192.168.3.0",
             "type":"MANAGEMENT"
         }
     ],
     "computes":
     [
         {
             "name": "red-router",
             "image": "ubuntu-14.04-server-cloudimg-amd64-disk1.img",
             "type": "KVM",
             "cpu": "1",
             "ram": "512",
             "networks":[
                {
                  "name":"net1",
                  "ip-address": "192.168.1.150"
                },
                {
                  "name":"net2",
                  "ip-address": "192.168.2.150"
                }
             ]
         },
         {
             "name": "phcd",
             "image": "ubuntu-ads",
             "type": "DOCKER",
             "networks":[
                {
                  "name":"net1",
                  "ip-address": "192.168.1.225"
                }
             ]
         },
         {
             "name": "stormshield",
             "image": "ubuntu-14.04-server-cloudimg-amd64-disk1.img",
             "type": "KVM",
             "cpu": "1",
             "ram": "512",
             "networks":[
                {
                  "name":"net2",
                  "ip-address": "192.168.2.200"
                },
                {
                  "name":"net3",
                  "ip-address": "192.168.3.200"
                }
             ]
         },
         {
             "name": "vSOP",
             "image": "ubuntu-ads",
             "type": "DOCKER",
             "networks":[
                {
                  "name":"net3",
                  "ip-address": "192.168.3.3"
                }
             ]
         }
     ]
   }
}"""

delete_service1="""
{
   "delete":{
      "network_service_type": "manpack", 
      "service_function_forwarder":
      [
         {
             "name": "net1"
         },
         {
             "name": "net2"
         },
         {
             "name": "net3"
         }
     ],
     "computes":
     [
         {
             "name": "stormshield",
             "type": "KVM"
         },
         {
             "name": "red-router",
             "type": "KVM"
         },
         {
             "name": "phcd",
             "type": "DOCKER",
             "networks":[
                {
                  "name":"net1"
                }
             ]
         },
         {
             "name": "vSOP",
             "type": "DOCKER",
             "networks":[
                {
                  "name":"net3"
                }
             ]
         }
     ]
   }
}"""

""" Emulate RPC client"""

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='127.0.0.1'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='nfvi.dd7cf9cf-dc99-468b-9b4a-60680f0bf05c',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return (self.response)

fibonacci_rpc = FibonacciRpcClient()

print("Requesting the RPC")
#response = fibonacci_rpc.call(service1)
response = fibonacci_rpc.call(delete_service1)
print("Response %r" % response)
