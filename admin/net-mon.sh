#!/bin/bash

echo "Service started on $(date)"

while true ; do
   if ifconfig wlan0 | grep -q "inet addr:" ; then
      sleep 60
   else
      echo "[$(date)]"  "Network connection down! Attempting reconnection."
      ifup --force wlan0
      sleep 10
   fi
done

