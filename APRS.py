#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import aprslib
import pdb

import Config

def init() :
	Config.AprsStat = "Not active"
	logging.debug("APRS init() done") 
	Config.Login = 0
	Config.AIS = aprslib.IS(Config.CALL, Config.PASSCODE, port=14580)
	Config.AIS.connect()
	Config.Login += 1

"""
def sendMsg( msg ) :
	logging.info("APRS Packet to sent: %s" , msg)
	logging.info("MSG: %s", msg)
	if (Config.EN_APRSIS) :
		try :
			AIS = aprslib.IS(Config.CALL, Config.PASSCODE, port=14580)
			AIS.connect()
			AIS.sendall(msg)
			AIS.close()
			Config.AprsStat = "Active"
			Config.MsgSent +=1
		except: 
			logging.info("APRS-IS upload failed")

	else :
		logging.debug("APRS-IS upload: %s",  Config.EN_APRSIS)
		Config.AprsStat = "Test"
	Config.LastPkt = msg
"""

def sendMsg( msg ) :
	logging.info("APRS Packet to sent: %s" , msg)
	logging.info("MSG: %s", msg)
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
		logging.debug("APRS-IS upload: %s",  Config.EN_APRSIS)
		Config.AprsStat = "Test"
	Config.LastPkt = msg



