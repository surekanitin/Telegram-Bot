#!/bin/sh
yum install python3
yum install pip3
pip3 install requirements.txt
python /home/nitin/Desktop/PROJECT/Telegram-Bot/Bots/bot.py &
python /home/nitin/Desktop/PROJECT/Telegram-Bot/Bots/covid_bot.py &
python /home/nitin/Desktop/PROJECT/Telegram-Bot/Bots/stock_bot.py &
python /home/nitin/Desktop/PROJECT/Telegram-Bot/Bots/weather_bot.py