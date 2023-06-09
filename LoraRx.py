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
	logger.info("WX sent: %s" % name)

def gotPacket(buffer) :
	message="".join(map(chr,buffer[0]))
	message=message[3:]
	#logger.info("RX Packet received: %s " %  message)
	Config.RxCount +=1
	addrend = message.find(":",5,20)
	message = message[:addrend] +  ",qAO," + Config.CALL + message[addrend:]
	APRS.sendMsg(message)

def init() :
	logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
	logger = logging.getLogger(__name__)

	loralib.init(1, Config.Frequ, Config.SR)
	Config.RxCount =0
	logger.info("init() done")
#	pdb.set_trace()


def main() :
	#bcTimer = RepeatedTimer(Config.BeaconIntervall, sendBeacon, msgBeaconStatus + str(rxCount)) 
	#wxTimer = RepeatedTimer(20, wx, "WX") 

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



