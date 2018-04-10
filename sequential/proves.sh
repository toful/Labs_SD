#!/bin/bash

nummappers="1 2 3 4 5 6 7 8 9 10"
operation="wc cw"
filename="sherlock.txt sherlock2.txt sherlock3.txt sherlock4.txt sherlock5.txt sherlock6.txt sherlock7.txt sherlock8.txt sherlock9.txt sherlock10.txt pg10.txt pg2000.txt"

for i in $nummappers;
do
	for j in $operation;
	do
		for k in $filename;
		do 
			echo $i $j $k
			echo "Aleix Careto"
			python mapreduce_sequential.py $i $j $k
		done
	done
done

exit 0