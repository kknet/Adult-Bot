#!/bin/sh

BOT_PATH=/root/Path
if [ ! -d $BOT_PATH/logs ]; then
mkdir $BOT_PATH/logs
fi
GREEN='\033[0;32m'
NORMAL='\033[0m'
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::           ${GREEN}PornBot by RaZoR ${NORMAL}               :::"
echo ":::                                			                 :::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::                        Start Posting                       :::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ""
echo "${GREEN}::: Ready :::${NORMAL}"
echo ""
echo "${GREEN}::: Log Service :::${NORMAL}"
cd $BOT_PATH; python runner.py > $BOT_PATH/logs/runner.log 2>&1
sleep 1

