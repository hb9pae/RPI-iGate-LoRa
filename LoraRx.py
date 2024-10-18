#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Lora Package handler, prepare headr info and send it to APRS-IS 
"""

__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__ = "hb9pae@gmail.com"


import loralib
import time
import pdb
import logging
#from threading import Timer
import threading
import aprslib
from datetime import datetime
import random

import APRS
import Config
import Display 

def wx(name):
	print("Send new %s!" % name)
	logging.info("WX sent: %s" %  name)

### LoraRX() neu 
def loraRX():
	buffer=loralib.recv()
	lock = threading.Lock()
	lock.acquire()
	if buffer[1] > 0 and buffer[5] == 0 :
		try:
			#print("RX Size: %d, PRSSI: %d, RSSI: %d, SNR %d" % (buffer[1], buffer[2], buffer[3], buffer[4]) )
			Config.PktSize = buffer[1]
			Config.PktRSSI = buffer[2]
			Config.RSSI = buffer[3]
			Config.SNR = buffer[4]
			message ="".join(map(chr,buffer[0][3:]))
			message = message.rstrip("\x00")
			# add iGate call to path
			addrend = message.find(":",5,40)
			message = message[:addrend] +  ",qAO," + Config.CALL + message[addrend:]
			APRS.sendMsg(message)

			Config.LastMsg =  message
			now = datetime.now()
			Config.LastRx = now.strftime("%Y-%m-%d %H:%M:%S") 
			Config.RxCount += 1
			#logging.info("RX Packet received, Size:%d, PRSSI:%d, RSSI:%d, SNR:%d, RxCount:%d" % (len(message), Config.PktRSSI, Config.RSSI, Config.SNR, Config.RxCount))
		except:
			Config.RxErr += 1
			logging.info("Error read RX-Buffer %s, Size: %d" % (buffer[0], buffer[1]) )

		lock.release()
		Display.display(2)

def init() :
	loralib.init(1, Config.Frequ, Config.SR)
	Config.RxCount =0
	logging.debug("LoRa RX init done")
#	pdb.set_trace()

def main() :
	while(True) :	
		#pdb.set_trace()
		loraRX() 
		time.sleep(0.1)

if __name__ == "__main__":
	init()
	main()



