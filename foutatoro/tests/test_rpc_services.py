#!/usr/bin/env python
# Author: Alioune BA

from foutatoro.agent.services.rpc_services import RpcServices
import json


""" testing the RPC server """
rpc = RpcServices()
rpc.start_rpc_service()