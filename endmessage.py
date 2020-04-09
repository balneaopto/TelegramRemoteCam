#!/usr/bin/env python3
#Used in go.sh to send a notification to the bot you have created, saying that remote control is terminated 
import telegram_send
from config import *  # This way you can use global variables from config.py directly
MSG = MSG_STOP
# Send a message to the bot you have created
telegram_send.send(messages=[MSG])
