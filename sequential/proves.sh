#!/bin/bash

nummappers="1 2 3 4 5 6 7 8 9 10"
operation="wc cw"
filename="../distributed_v1/HTTPServer/big.txt ../distributed_v1/HTTPServer/pg10.txt ../distributed_v1/HTTPServer/pg2000.txt"

for i in $nummappers;
do
	for j in $operation;
	do
		for k in $filename;
		do 
			echo $i $j $k
			python mapreduce_sequential.py $i $j $k
		done
	done
done

exit 0
