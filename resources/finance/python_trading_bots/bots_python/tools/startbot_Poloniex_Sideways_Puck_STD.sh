#!/bin/sh
echo "Starting Bot Poloniex Sideways Puck STD"
date
nohup /usr/bin/python3 -u /home/Poloniex_Sideways_Puck_STD/main.py > /home/logs/Poloniex_Sideways_Puck_STD.log &
