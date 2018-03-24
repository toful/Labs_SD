#!/bin/bash

#This script will run automatically 3 server, a registry for this servers and a client in three diferent gnome-terminals
#Client port needed as an argument
# Argument 1: Port
# Arguemnt 2: Registry IP
# Argument 3: Mode d'operació: wc|cw
# Argument 4: file input
# Argument 5: IP from web server
# Argument 6: Número de mappers 


# Parameters of client.py:
# 1: Port used to establish the communication
# 2: Registry IP (Port is hardcoded to be 6000)
# 3: Operation to use [wc|cw]
# 4: Input file from HTTP Server
# 5: IP from web server
if [ $# -lt 5 ]
then
	echo "ERROR: Client Port needed as an argument!"
	exit 1
fi
cd HTTPServer
gnome-terminal -e "python HTTPServer.py"
cd ..
gnome-terminal -e "python registry.py"

for ((i=1;i<=$6+2;i++)); do
	gnome-terminal -e "python server.py $(($1 + $i))"
done
gnome-terminal -e "python client.py $1 $2 $3 $4 $5"
exit 0