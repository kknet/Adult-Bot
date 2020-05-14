#!/bin/sh

GREEN='\033[0;32m'
NORMAL='\033[0m'
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::           ${GREEN}PornBot by RaZoR ${NORMAL}   	         :::"
echo ":::                                			                 :::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::                    Stopping Posting                        :::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

echo "Stop Runner Daemon"
pkill -9 runner.py 
sleep 3
echo "Clear Cache"
echo 3 > /proc/sys/vm/drop_caches
sleep 1
