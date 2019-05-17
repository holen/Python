#!/bin/bash

for i in 0 1 2 3 4 
do
    python /home/zhl/rpc/client.py &
    # wait
done
