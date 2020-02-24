#!/bin/sh
echo "Starting Bot Okcoin Ticker"
date
nohup /usr/bin/python3 -u /home/Okcoin-Ticker/main.py >> /home/logs/okcoin-Ticker.log &
