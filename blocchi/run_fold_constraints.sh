#!/bin/bash

cd Rfam_13
mkdir folded
cd constraints
for i in `ls *.constraints`;do echo ${i}; RNAfold --noPS < ${i} > ../folded/${i%%.constraints}.folded;done
cd ../folded
for i in `ls *.folded`;do awk 'BEGIN{c=1}{if(c==1){print "@"substr($1,2);c+=1}else if(c==2){print $1;c+=1}else{print "+";print$1;c=1}} ' ${i} > ${i%%.folded}.fastq;done
