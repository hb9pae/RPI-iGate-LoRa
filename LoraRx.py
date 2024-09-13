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
from threading import Timer
import aprslib
from datetime import datetime
import random

import APRS
import Config
import Display 

def wx(name):
	print("Send new %s!" % name)
	logging.info("WX sent: %s" % name)

def gotPacket(buffer) :
	now = datetime.now()
	#print("RX Size: %d, PRSSI: %d, RSSI: %d, SNR %d" % (buffer[1], buffer[2], buffer[3], buffer[4]) )
	Config.PktSize = buffer[1]
	Config.PktRSSI = buffer[2]
	Config.RSSI = buffer[3]
	Config.SNR = buffer[4]
	try :
		message ="".join(map(chr,buffer[0]))
		message = message[3:]
		Config.LastRx = now.strftime("%Y-%m-%d %H:%M:%S") 
		Config.RxCount += 1
		logging.info("RX Packet received, Size:%d, PRSSI:%d, RSSI:%d, SNR:%d, RxCount:%d" % (len(message[3:]), Config.PktRSSI, Config.RSSI, Config.SNR, Config.RxCount))
		#pdb.set_trace()
	except:
		Config.RxError += 1
		logging.info("Error read RX-Buffer %s, Size: %d" % (buffer[0], buffer[1]) )
	try :
		pkt = aprslib.parse(message)
		Config.From = pkt.get("from")
		Config.To = pkt.get("to")
		Display.display(2)
		#pdb.set_trace()
	except:
		#pdb.set_trace()
		logging.info("Error RX-Buffer validation %s, Size: %d" % (buffer[0], buffer[1]) )

	# add iGate call to path
	addrend = message.find(":",5,40)
	message = message[:addrend] +  ",qAO," + Config.CALL + message[addrend:]
	Config.LastMsg =  message
	APRS.sendMsg(message)

def init() :
	loralib.init(1, Config.Frequ, Config.SR)
	Config.RxCount =0
	logging.debug("LoRa RX init done")
#	pdb.set_trace()

def loraRX() :
	msg=loralib.recv()
	if msg[1] > 0 and msg[5] == 0 :
		gotPacket(msg)

def main() :
	while(True) :	
		#pdb.set_trace()
		loraRX() 
		time.sleep(0.1)

if __name__ == "__main__":
	init()
	main()



