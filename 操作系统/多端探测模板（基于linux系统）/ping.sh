#!/bin/bash
destination_ip=${1}

ping_result=$(LANG=en_US ping -q -c 2 $destination_ip 2>&1)
if grep -q 'not known' <<< "${ping_result}";then
    echo "{\"status\":\"目标IP或主机名错误\"}"
    exit 1
fi
# echo "${ping_result}"
loss=$(echo ${ping_result} | grep -oP '[0-9]+% packet loss')
if [ $? -eq 0 ];then
    loss_1=$(awk -F\% '{print $1}' <<< "$loss")
else
    echo "{\"status\":\"PING结果无法解析\"}"
    exit 1
fi

if [ ${loss_1} -eq 100 ];then
    echo "{\"loss\":${loss_1},\"status\":0}"
else
    sec=$(echo ${ping_result} | grep -oP 'rtt min\/avg\/max\/mdev = \K[0-9]+\.[0-9]+\/[0-9]+\.[0-9]+\/[0-9]+\.[0-9]+\/[0-9]+\.[0-9]+ ms')
    if [ $? -eq 0 ];then
        sec_min=$(awk -F \/ '{print $1}' <<< "$sec")
        sec_avg=$(awk -F \/ '{print $2}' <<< "$sec")
        sec_max=$(awk -F \/ '{print $3}' <<< "$sec")
        echo "{\"loss\":${loss_1},\"status\":1,\"sec\":${sec_max}}"
    else
        echo "{\"loss\":${loss_1},\"status\":1,\"sec\":\"PING结果无法解析\"}"
        exit 1
    fi
fi

