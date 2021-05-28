#!/bin/bash

for i in {1..9}
do
	> data$i.txt
done

for i in {1..29}
do
	for j in {1..9}
	do
		echo $i >> data$j.txt
		grep fit ./PS$i/P$j/best.lint | sort -n >> data$j.txt
		echo '' >> data$j.txt
	done
done
