#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Receives Lora Package and submit it to APRS.FI 
"""

__version__ = "1.0.1"
__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2023"
__email__ = "hb9pae@gmail.com"


import loralib
import time
import pdb
from hexdump import hexdump
import logging
from threading import Timer
import aprslib

import APRS
import Config

def wx(name):
	print("Send new %s!" % name)
	logging.info("WX sent: %s" % name)

def gotPacket(buffer) :
	message="".join(map(chr,buffer[0]))
	message=message[3:]
	logging.info("RX Packet received")
	Config.RxCount +=1
	addrend = message.find(":",5,20)
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



