#!/bin/bash

#This script will run automatically 3 server, a registry for this servers and a client in three diferent gnome-terminals
#Client port needed as an argument

if [ $# -lt 1 ]
then
	echo "ERROR: Client Port needed as an argument!"
	exit 1
fi
gnome-terminal -e "python registry.py"
gnome-terminal -e "python server.py 1234"
gnome-terminal -e "python server.py 1235"
gnome-terminal -e "python server.py 1236"
gnome-terminal -e "python client.py $1"
exit 0