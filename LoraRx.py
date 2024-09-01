#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Lora Package handler, prepare headr info and send it to APRS-IS 
"""

__version__ = "1.0.2"
__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__ = "hb9pae@gmail.com"


import loralib
import time
import pdb
import logging
from threading import Timer
import aprslib
from datetime import datetime
import random

import APRS
import Config

def wx(name):
	print("Send new %s!" % name)
	logging.info("WX sent: %s" % name)

def gotPacket(buffer) :
	now = datetime.now() 
	#logging.debug("RX Size: %d, PRSSI: %d, RSSI: %d, SNR %d" % (buffer[1], buffer[2], buffer[3], buffer[4]) )
	Config.PktRSSI = buffer[2]
	Config.RSSI = buffer[3]
	Config.SNR = buffer[4]
	message="".join(map(chr,buffer[0]))
	#pdb.set_trace()
	# Einige Tracker schliessen den MSG String mit einem 0x00 ab, wir entfernen non-ASCII am Ende des Strings
	lastchar = ord(message[-1])
	if (lastchar < 32) :
		message = message[3:-1]
	else :
		message=message[3:]
	Config.LastMsg=now.strftime("%Y-%m-%d, %H:%M:%S: ") + message
	Config.RxCount +=1
	logging.info("RX Packet received, Size:%d, PRSSI:%d, RSSI:%d, SNR:%d, RxCount:%d" % (len(message), Config.PktRSSI, Config.RSSI, Config.SNR, Config.RxCount))
	addrend = message.find(":",5,40)
	# add iGate call to path
	message = message[:addrend] +  ",qAO," + Config.CALL + message[addrend:]
	APRS.sendMsg(message + (" " * random.randint(0,5)) )

def init() :
	loralib.init(1, Config.Frequ, Config.SR)
	Config.RxCount =0
	logging.debug("LoRa RX init done")
#	pdb.set_trace()

def main() :
	while(True) :
		msg=loralib.recv()
                if msg[1] > 0 and msg[5] == 0 :
			logging.info("Packet received, no CRC error")
			#pdb.set_trace()
			gotPacket(msg)
			HMI.display(3)  # display received Packaage
		time.sleep(0.1)

if __name__ == "__main__":
	init()
	main()



