#!/bin/bash

> allData.txt

for i in {1..29} # All PSs
do
	for j in {1..9} # All Profiles
	do
		echo "PS $i - Profile $j" >> allData.txt
		grep fit ./PS$i/P$j/best.lint | sort -n >> allData.txt
		echo '' >> allData.txt
	done
done