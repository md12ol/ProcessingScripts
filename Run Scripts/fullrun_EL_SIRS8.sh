#!/bin/bash
#This script facilitates multiple settings to run on different processors

#All processes end when completed compilation

#Run line
#nohup ./template.sh &

#The lines below run the simulation with the correct profile, output and parameters
: ' Parameter Settings for setting.sh
$1 - Toggle Density
$2 - Hop Density
$3 - Add Density
$4 - Delete Density
$5 - Swap Density
$6 - Local Toggle Density
$7 - Local Add Density
$8 - Local Delete Density
$9 - Null Density
'

: ' Run line params
$1 - Folder making mode?
$2-$10 - Densities
$11 - Time Removed
$12 - Output Path from ./Output/
$13 - Profile Num
'
# Compiles the java files
javac *.java

# Makes the folders
java Main true 0 0 0 0 0 0 0 0 0 0 0 0

#Removes the old outputs if they exist then creates all the directories for a new run
> nohup.out #Clears the nohup.out file

PSnum=1
running=0

#While there are more Paramater Settings to process
while read -r line
do
	#Take the line and separate the individual parameters into an array
	IFS=' ' read -a ps <<< "$line"

	if [[ ${running} == 8 ]]
	then
	sleep 3h
	running=0
	fi

	java Main false ${ps[0]} ${ps[1]} ${ps[2]} ${ps[3]} ${ps[4]} ${ps[5]} ${ps[6]} ${ps[7]} ${ps[8]} 8 PS${PSnum} 0 &

	PSnum=$(( $PSnum + 1 ))
	running=$(( $running + 1 ))

done <"ParameterSettings.txt"