#!/bin/bash
#######################################################################
##  The shell is due to move one month ago that the user exported fiels
##  create by holen

Base="/usr/local/application/elink2/userfiles"

Division=`ls -1 $Base | grep '^[0-9]'`

for div in $Division
do
	ExportDir=`ls -1 $Base/$div | grep export`
	for dir in $ExportDir
	do
		tardir="/mnt/$div/$dir"
		if [ ! -d $tardir ];then
			mkdir -p $tardir
			if [ $? != 0 ];then
				echo "mkdir dir is false ..." >> /tmp/moveUserfie.log
				exit 1
			fi
		fi
		find ${Base}/${div}/${dir}/ -type f -mtime +30 -exec mv {} $tardir \;
	done
done
			
