#!/bin/bash
#creato da NoiSe

###launch Beagle (AMBeR) -- different alphabets, differents bonuses

for mat in friendlyMats/*
do
	echo -------------------------------------------------------
	echo beagling $mat
	echo -------------------------------------------------------
	
	MATRIX=$mat
	ext_=${mat#*_}
	EXT=${ext_%.*}
	for bench in datasets/set1/*
	do
		SET1=$bench
		settmp=datasets/set2/${bench##*/}
		SET2=${settmp%1}2
		tmp=${bench##*/}
		tmp2=${tmp%%_*}
		###Bonus
		for BONUS in $(seq 0.0 0.1 10.0)
		do
			BONUSLABEL=${BONUS/./}
			OUT=out/${EXT}_${tmp2}_${BONUS}.out
			SECONDS=0

			#do the work only if the file is not already there!!!
			if [ ! -f $OUT ]
			then

				echo java -jar AMBeR.jar -p -m $MATRIX -b $BONUS -input1 $SET1 -input2 $SET2 -outfile $OUT 
				java -jar AMBeR.jar -p -m $MATRIX -b $BONUS -input1 $SET1 -input2 $SET2 -outfile $OUT 

				duration=$SECONDS
				echo $BONUS
				#echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed for a complete cycle (total of 80bonus * 4datasets cycles))."
			fi
		done
	done
	

done
