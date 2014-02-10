#/bin/bash

# Source function library.
. /etc/init.d/functions

cd /domaindata/
Tdate=`date +%Y-%m-%d`
Ttime=`date +'%m-%d %H:%M:%S'`
LogFile="/tmp/log/domain.$Tdate.log"
echo " " >> $LogFile
echo "[`date +'%m-%d %H:%M:%S'`] the program is begin ..." >> $LogFile

Get_Domain(){
	if [ -f /domaindata/source/$1 ];then
		LineNum=0
		Dir="/domaindata/${1%.txt}"
		if [ ! -d $Dir ];then
			mkdir -p $Dir 
			if [ $? == 0 ];then
				echo "[`date +'%m-%d %H:%M:%S'`] mkdir $Dir ok ..." >> $LogFile
			else
				echo "[`date +'%m-%d %H:%M:%S'`] mkdir $Dir False" >> $LogFile
				exit 1
			fi
		else
			mv $Dir ${Dir}.${Tdate}.$$
			if [ $? == 0 ];then
				echo "[`date +'%m-%d %H:%M:%S'`] mv $Dir ok ..." >> $LogFile
			else	
				echo "[`date +'%m-%d %H:%M:%S'`] mv $Dir False" >> $LogFile
				exit 1
			fi
			mkdir -p $Dir
			if [ $? == 0 ];then
				echo "[`date +'%m-%d %H:%M:%S'`] mkdir $Dir ok ..." >> $LogFile
			else	
				echo "[`date +'%m-%d %H:%M:%S'`] mkdir $Dir False" >> $LogFile
				exit 1
			fi
		fi
		mv /domaindata/source/$1 $Dir 
		if [ $? == 0 ];then
			echo "[`date +'%m-%d %H:%M:%S'`] mv /domaindata/source/$1 to $Dir ok ..." >> $LogFile
		else
			echo "[`date +'%m-%d %H:%M:%S'`] mv /domaindata/source/$1 to $Dir False" >> $LogFile
                        exit 1
		fi
		cd $Dir
		if [ $? == 0 ];then
                        echo "[`date +'%m-%d %H:%M:%S'`] cd $Dir ok ..." >> $LogFile
                else
                        echo "[`date +'%m-%d %H:%M:%S'`] cd $Dir False" >> $LogFile
                        exit 1
                fi
		var=`head -n 1 $1 |awk -F'[ ,]+' '{for(i=1;i<=NF;i++) if($i~/@/) print i}'`
		RETVAL=$?
		if [ "$var" != "" ] && [ $RETVAL == 0 ];then
			echo "[`date +'%m-%d %H:%M:%S'`] the file first line's email field is $var ..." >> $LogFile
		else
			echo "[`date +'%m-%d %H:%M:%S'`] the file first line is null or no email field ..." >> $LogFile
			sed -i '1d' $1
			var=`sed -n '2p' $1 |awk -F'[ ,]+' '{for(i=1;i<=NF;i++) if($i~/@/) print i}'`
			if [ $RETVAL == 0 ];then
				echo "[`date +'%m-%d %H:%M:%S'`] the file second line's email field is $var ..." >> $LogFile
			else
				echo "[`date +'%m-%d %H:%M:%S'`] the file second line is null or no email field ..." >> $LogFile
				exit 1
			fi
		fi
		awk -F'[ ,]' '{print $var}' var="$var" $1 > address.txt
		if [ $? == 0 ];then
			echo "[`date +'%m-%d %H:%M:%S'`] get email field ok ..." >> $LogFile
		else
                        echo "[`date +'%m-%d %H:%M:%S'`] get email field false ..." >> $LogFile
                        exit 1
		fi
	else
		exit 1
	fi

	cat address.txt | grep @ > email.txt
	if [ $? == 0 ];then
                echo "[`date +'%m-%d %H:%M:%S'`] remove the no @ email address ok ..." >> $LogFile
        else
                echo "[`date +'%m-%d %H:%M:%S'`] remove the no @ email address false ..." >> $LogFile
                exit 1
        fi
	sed -i -e '/\//d' -e 's/"//g' -e 's/^M//g' -e '/+/d' -e '/=/d' -e '/^@/d' email.txt
	if [ $? == 0 ];then
                echo "[`date +'%m-%d %H:%M:%S'`] remove the invalid email address ok ..." >> $LogFile
        else
                echo "[`date +'%m-%d %H:%M:%S'`] remove the invalid email address false ..." >> $LogFile
                exit 1
        fi

	for low in `cat email.txt`
	do
	     	echo $low >> ${low#*@}.txt
		#echo $low >> `tr '[A-Z' '[a-z]' <<< "${low#*@}"`.txt
		[ $? == 0 ] && ((++LineNum))
	done

        echo "[`date +'%m-%d %H:%M:%S'`] the file $1 exec $LineNum lines ..." >> $LogFile

	array=(qq.com.txt vip.qq.com.txt sina.com.txt sina.com.cn.txt sina.cn.txt yahoo.com.txt yahoo.cn.txt yahoo.com.cn.txt 163.com.txt 126.com.txt sohu.com.txt 21cn.com.txt tom.com.txt gmail.com.txt)
	TarDir="/address/${1%.txt}"
	if [ ! -d $TarDir ];then
		mkdir -p $TarDir 
		if [ $? == 0 ];then
                	echo "[`date +'%m-%d %H:%M:%S'`] mkdir $TarDir ok ..." >> $LogFile
                else
                        echo "[`date +'%m-%d %H:%M:%S'`] mkdir $TarDir False" >> $LogFile
                        exit 1
                fi
	else
		mv $TarDir ${TarDir}.$Tdate.$$
		if [ $? == 0 ];then
                        echo "[`date +'%m-%d %H:%M:%S'`] mv $TarDir ok ..." >> $LogFile
                else
                        echo "[`date +'%m-%d %H:%M:%S'`] mv $TarDir False" >> $LogFile
                        exit 1
                fi
		mkdir -p $TarDir 
		if [ $? == 0 ];then
                        echo "[`date +'%m-%d %H:%M:%S'`] mkdir $TarDir ok ..." >> $LogFile
                else
                        echo "[`date +'%m-%d %H:%M:%S'`] mkdir $TarDir False" >> $LogFile
                        exit 1
                fi
	fi
	for var in ${array[@]}
	do
		if [ -e $var ];then
			cp $var $TarDir && echo "[`date +'%m-%d %H:%M:%S'`] cp $var to $TarDir ok ..." >> $LogFile
		else
			echo "[`date +'%m-%d %H:%M:%S'`] the file $var doesn't exist ..." >> $LogFile
		fi
	done
}

for tfile in `ls -1 /domaindata/source`
do
	echo "[`date +'%m-%d %H:%M:%S'`] the file $tfile is doing now ..." >> $LogFile
	Get_Domain "$tfile"
	[ $? == 0 ] && echo "[`date +'%m-%d %H:%M:%S'`] the file $tfile is done ... " >> $LogFile
done

echo "[`date +'%m-%d %H:%M:%S'`] the program is end ..." >> $LogFile
