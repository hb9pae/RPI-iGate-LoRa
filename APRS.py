#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import aprslib
import pdb

import Config

#log = logging.getLogger(__name__)
#log.setLevel(logging.ERROR)


def init() :
	Config.AprsStat = "Not active"
	logging.debug("APRS init() done") 

def sendMsg( msg ) :
	logging.info("APRS Packet to sent: %s" , msg)
	if (Config.EN_APRSIS) :
		AIS = aprslib.IS(Config.CALL, Config.PASSCODE, port=14580)
		AIS.connect()
		AIS.sendall(msg)
		AIS.close()
		Config.AprsStat = "Active"
		Config.MsgSent +=1
	else :
		logging.debug("APRS-IS upload: %s",  Config.EN_APRSIS)
		Config.AprsStat = "Test"
	Config.LastPkt = msg



