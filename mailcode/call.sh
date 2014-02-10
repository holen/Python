#!/bin/bash

export IGNOREEOF=1
#export ANT_HOME=/usr/local/application/apache-ant-1.6.2
export BS_HOME=/usr/local/application/elink2/backapp
export JAVA_HOME=/data/elink/java/jdk1.6
export PATH=$PATH:$ANT_HOME/bin:$JAVA_HOME/bin

echo $@
#java -jar /home/upgrade/shells/cmd-invoker.jar com.yinhoo.backend.InvokeCommandMain $@
java -jar /home/upgrade/shells/cmd-invoker.jar $@
