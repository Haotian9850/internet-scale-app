#!/bin/sh
while [ true ]
do
    sudo docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/main.py
    sleep 60
done