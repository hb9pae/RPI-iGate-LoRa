#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Lora Package handler, prepare headr info and send it to APRS-IS 
"""

__version__ = "1.0.1"
__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2023"
__email__ = "hb9pae@gmail.com"


import loralib
import time
import pdb
import logging
from threading import Timer
import aprslib
from datetime import datetime

import APRS
import Config

def wx(name):
	print("Send new %s!" % name)
	logging.info("WX sent: %s" % name)

def gotPacket(buffer) :
	now = datetime.now() 
	logging.info("RX Size: %d, PRSSI: %d, RSSI: %d, SNR %d" % (buffer[1], buffer[2], buffer[3], buffer[4]) )
	Config.PktRSSI = buffer[2]
	Config.RSSI = buffer[3]
	Config.SNR = buffer[4]
	message="".join(map(chr,buffer[0]))
	message=message[3:]
	Config.LastMsg=now.strftime("%Y-%m-%d, %H:%M:%S: ") + message
	logging.info("RX Packet received Size: %d, PRSSI: %d, RSSI: %d, SNR %d" % (len(message), Config.PktRSSI, Config.RSSI, Config.SNR))
	Config.RxCount +=1
	addrend = message.find(":",5,40)
	# add iGate call to path
	message = message[:addrend] +  ",qAO," + Config.CALL + message[addrend:]
	APRS.sendMsg(message)

def init() :
	loralib.init(1, Config.Frequ, Config.SR)
	Config.RxCount =0
	logging.info("LoRa RX init done")
#	pdb.set_trace()


def main() :
	try:
		while(1) :
			msg=loralib.recv()
			if msg[5] == 0 and msg[1] > 0:
				gotPacket(msg)
			time.sleep(0.05) # your long-running job goes here...

	finally:
		bcTimer.stop() 
		wxTimer.stop() 

if __name__ == "__main__":
	init()
	main()



