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
	else :
		logger.info("APRS-IS: %s" % Config.APRSIS)
		Config.AprsStat = "Test"
	Config.LastPkt = msg
	logger.info("APRS Packet sent: %s" % msg)


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

