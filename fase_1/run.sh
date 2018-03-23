#!/bin/bash

#This script will run automatically 3 server, a registry for this servers and a client in three diferent gnome-terminals
#Client port needed as an argument
# Argument 1: Port
# Arguemnt 2: Registry Port
# Argument 3: Mode d'operació: wc|cw
# Argument 4: Número de mappers 

if [ $# -lt 1 ]
then
	echo "ERROR: Client Port needed as an argument!"
	exit 1
fi
gnome-terminal -e "python registry.py"

for ((i=1;i<=$4+1;i++)); do
	gnome-terminal -e "python server.py $(($1 + $i))"
done
gnome-terminal -e "python client.py $1 $2 $3"
exit 0