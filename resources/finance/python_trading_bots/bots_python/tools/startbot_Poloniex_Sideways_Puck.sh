#!/bin/sh
echo "Starting Bot Poloniex Sideways Puck"
date
nohup /usr/bin/python3 -u /home/Poloniex_Sideways_Puck/main.py > /home/logs/Poloniex_Sideways_Puck.log &
