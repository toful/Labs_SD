#!/bin/bash

#This script will run automatically 3 server and a client in three diferent gnome-terminals
#Client port needed as an argument

if [ $# -lt 1 ]
then
	echo "ERROR: Client Port needed as an argument!"
	exit 1
fi
gnome-terminal -e "python server.py $(($1+1))"
gnome-terminal -e "python server.py $(($1+2))"
gnome-terminal -e "python server.py $(($1+3))"
gnome-terminal -e "python client.py $1 $(($1+1)) $(($1+2)) $(($1+3))"
exit 0
