#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Lora Package handler, prepare headr info and send it to APRS-IS 
2024-10-18 HB9PAE fast version, tread lock
"""

__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__ = "hb9pae@gmail.com"


import loralib
import time
import pdb
import Utils
import threading
import aprslib
from datetime import datetime
import random
import HMI
import APRS
import Config

global buffer 

"""
def wx(name):
	Utils.logEvent("WX sent: %s" %  name)
"""

def LoraRx():
	buffer=loralib.recv()
	lock = threading.Lock()
	if buffer[1] > 0 and buffer[5] == 0 :
		lock.acquire()
		Config.TS = time.time()
		Config.PktSize = buffer[1]
		Config.PktRSSI = buffer[2]
		Config.RSSI = buffer[3]
		Config.SNR = buffer[4]
		#pdb.set_trace()
		_buff = buffer[0][3:]
		lock.release()

		message ="".join(map(chr,_buff))
		message = message.rstrip("\x00")
		# add iGate call to path
		addrend = message.find(":",5,40)
		message = message[:addrend] +  ",qAO," + Config.ConfigDict["call"] + message[addrend:]
		#pdb.set_trace()
		APRS.sendMsg(message)
		Config.LastRx = Utils.datestring()  
		Config.LastMsg =  message
		Config.NewMsg = True
		Config.RxCount += 1
		time.sleep(0.0001)

def init() :
	loralib.init(1, Config.Frequ, Config.SR)
	Config.RxCount =0

def main() :
	while(True) :	
		#pdb.set_trace()
		loraRX() 
		time.sleep(0.1)

if __name__ == "__main__":
	init()
	main()



