#!/usr/bin/python
# Author BA Alioune

import requests
import json

""" Ce code reprend en python ce qu'on a fait avec la commande curl en cours"""

"""Authentication"""
authentication_data='{"auth":  { "tenantName": "admin", "passwordCredentials": { "username": "admin", "password": "admin" } } }'

openstack_authentication_url = 'http://192.168.150.15:5000/v2.0/tokens'

response = requests.post(openstack_authentication_url, data=authentication_data)

"Get the response of openstack in JSON format "
json_response =  response.json()

"""Get the token"""
jsonData = json_response["access"]
token = jsonData["token"]["id"]
print token

"""List all network in OpenStack"""
openstack_network_url='http://192.168.150.15:9696/v2.0/networks.json'

response = requests.get(openstack_network_url,headers={'X-Auth-Token': str(token), 'Accept': 'application/json'})

print ("Printing all openstack network in JSOn format")
print response.json()

"""
normalement l'utilisateur s'authentifie une fois et acceder a ses document sur swift
vous de vous inspirer sur ces deux exemples et de faire les actions necessaires avec l'url de l API de Swift
ATTENTION: j'ai declare la variable authentication_data comme etant statique mais pour votre Appli elle doit etre dynamique
car tous les utilisateur n'ont pas les memes identifiants ni n'appartiennent aux memes tenant/projets
"""