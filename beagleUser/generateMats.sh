#!/bin/bash
#created by NoiSe

#for pair of mat and map in startingMats create friendlyMat

for mat in startingMats/*
do
	echo ------------------------------------------------------------
	echo  working through file: $mat
	echo ------------------------------------------------------------

	EXT=${mat#*_}
	
	MAT=$mat
	MAP=startingMaps/alphamap_$EXT

	echo Extension: $EXT
	echo Alphabet Mapping: $MAP
	echo Starting Substitution Matrix: $MAT

	python alphaSubToBeagleFriendly.py -e $EXT -m $MAT -a $MAP

	echo ------------------------------------------------------------
	echo  written file: friendlyMats/convertedMatrix_$EXT
	echo ------------------------------------------------------------


done
