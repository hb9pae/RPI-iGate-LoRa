#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import aprslib
import pdb

import Config


def init() :
	Config.AprsStat = "Not active"

def sendMsg( msg ) :
	if (Config.APRSIS.lower() in ['true', '1', 'yes'] ) :
		AIS = aprslib.IS(Config.CALL, Config.PASSCODE, port=14580)
		AIS.connect()
		AIS.sendall(msg)
		AIS.close()
		Config.AprsStat = "Active"
		Config.MsgSent +=1
	else :
		logging.info("APRS-IS upload: %s",  Config.APRSIS)
		Config.AprsStat = "Test"
	Config.LastPkt = msg
	logging.info("APRS Packet sent: %s" , msg)



