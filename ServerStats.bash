#!/bin/bash


cpuUsage=$(top -bn1 | grep Cpu | awk '{print $2 + $4}')
ramUsage=$(top -bn1 | grep 'MiB Mem' | awk '{print $8}')
ramTotal=$(top -bn1 | grep 'MiB Mem' | awk '{print $4}')
storageUsage=$(df -h . | grep / | awk '{print $3}')
storageAvailable=$(df -h . | grep / | awk '{print $4}')
storageTotal=$(df -h . | grep / | awk '{print $2}')

#sshStatus=
#apacheStatus=


> stats.txt
echo "CPU Usage - "$cpuUsage"%" >> stats.txt
echo "RAM Usage - " $ramUsage "MiB" >> stats.txt
echo "RAM Total - "$ramTotal "MiB" >> stats.txt
echo "Storage Used - "$storageUsage >> stats.txt
echo "Storage Available - "$storageAvailable >> stats.txt
echo "Storage Total - "$storageTotal >> stats.txt

#echo "CPU Usage: "$cpuUsage"%"\n"RAM Usage:" $ramUsage "MiB"\n"RAM Total: "$ramTotal "MiB"\n"Storage Used: "$storageUsage\n"Storage Available: "$storageAvailable\n"Storage Total: "$storageTotal>> stats.txt