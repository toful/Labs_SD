# MapReduce
MapReduce implementation in the Distributed Sistems Subject using pyActor.

## Pre-requisites

This version has been implemented over pyActor
More information about this python actor middleware in [Pyactor](https://github.com/pedrotgn/pyactor)

'''
pip install pyactor
'''

## Functioning

### Arguments

- MASTER_PORT/SLAVE_PORT: Port used to establish the communication
- REGISTRY_IP: Registry IP (Port is hardcoded to be 6000)
- OPERATION: Operation to use [wc|cw]
- INPUT_FILE:  Input file from HTTP Server
- WEB_SERVER_IP: IP from web server
- HOST_IP: IP de la màquina host 


Running the distributed version:

1- Run the HTTPServer
'''
python HTTPServer.py
'''

2- Run the Registry
'''
python registry.py
'''

3- Run as slaves as you will have (at least 3)
'''
python server.py SLAVE_PORT
'''

4- Run the master
'''
python client.py MASTER_PORT REGISTRY_IP OPERATION INPUT_FILE WEB_SERVER_IP HOST_IP
'''


## Authors
* ** Aleix Mariné Tena** - [AleixMT](https://github.com/AleixMT)
* ** Cristòfol Daudén Esmel** - [toful](https://github.com/toful)