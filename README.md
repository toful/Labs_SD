# MapReduce
MapReduce implementation in the Distributed Sistems Subject using pyActor.

## Pre-requisites

This version has been implemented over pyActor
More information about this python actor middleware in [Pyactor](https://github.com/pedrotgn/pyactor)

```
pip install pyactor
```

CodeHealth by [Codacy](https://codacy.com): 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/efcde4633c4840e883419dd586b3f21b)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=toful/MapReduce&amp;utm_campaign=Badge_Grade)

## Functioning

### Arguments

We need to explain some tags used as arguments:

- MASTER_PORT/SLAVE_PORT: Port used to establish the communication
- REGISTRY_IP: Registry IP (Port is hardcoded to be 6000)
- OPERATION: Operation to use [wc|cw]
- INPUT_FILE:  Input file from HTTP Server
- WEB_SERVER_IP: IP from web server
- HOST_IP: IP from self-host
- NUM_MAPPERS: Number of mappers used in operation.

We implemented two versions of MapReduce: 

#### Sequential

Sequential version of the software runs all operation in the client machine. You can find it in 'Sequential' folder. To run it:

```
python mapreduce_sequential.py INPUT_FILE OPERATION NUM_MAPPERS
```

#### Distributed:

Distributed version runs MapReduce with the possibility of using diferent machines instead of doing operations in local. This version include the use of advanced features such as an HTTPServer for distributing input files, an actor which splits the input file or the use of a registry to avoid managing too many IP directions.

You can run this software automatically using the script run.sh. This script initializes as many terminals as needed for the execution. 

```
./run.sh SLAVE_PORT REGISTRY_IP OPERATION INPUT_FILE WEBSERVER_IP HOST_IP NUM_MAPPERS
```

Also you can run it manually:

1- Run the HTTPServer
```
python HTTPServer.py
```

2- Run the Registry
```
python registry.py
```

3- Run as slaves as you will have (at least 3)
```
python server.py SLAVE_PORT
```

4- Run the master
```
python client.py MASTER_PORT REGISTRY_IP OPERATION INPUT_FILE WEB_SERVER_IP HOST_IP
```

You can also validate our solution massively using the script proves.sh. This script uses run.sh for running the MapReduce m*n*o times. Where m is the number of files, n the number of functions and o the number of mappers. This generates a big amount of output data. 

This data is hardcoded inside the script and it's easily modificable. proves.sh does not need any argument.

```
./proves.sh
```

## Authors

* **Aleix Mariné Tena** - [AleixMT](https://github.com/AleixMT)
* **Cristòfol Daudén Esmel** - [toful](https://github.com/toful)
