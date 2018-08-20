#!/bin/bash
word=$1
for i in $word
do 
	printf "\x$i"
done
printf "\n"
