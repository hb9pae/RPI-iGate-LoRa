#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import aprslib
import pdb

import Config


__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__ = "hb9pae@gmail.com"

def init() :
	Config.AprsStat = "Not active"
	Config.Login = 0
	if (Config.EN_APRSIS) :
		try :
			Config.AIS = aprslib.IS(Config.CALL, Config.PASSCODE, port=14580)
			Config.AIS.connect()
			Config.Login += 1
		except: 
			logging.info("APRS-IS upload failed")
	logging.debug("APRS init() done") 

def sendMsg( msg ) :
	logging.info("APRS Packet to send: %s" , msg)
	#logging.info("MSG: %s", msg)
	if (Config.EN_APRSIS) :
		#pdb.set_trace()
		if not Config.AIS._connected  :
			Config.AIS = aprslib.IS(Config.CALL, Config.PASSCODE, port=14580)
			Config.AIS.connect()
			Config.Login += 1
			logging.info("APRS-IS Login")
		try :
			Config.AIS.sendall(msg)
			Config.AprsStat = "Active"
			Config.MsgSent +=1
		except: 
			logging.info("APRS-IS upload failed")

	else :
		logging.info("APRS-IS upload: %s",  Config.EN_APRSIS)
		Config.AprsStat = "Test"
	Config.LastPkt = msg



