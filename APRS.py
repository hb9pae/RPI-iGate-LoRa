#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import aprslib
import pdb

import Globals


def init() :
	#Globals.BeaconTxt = Globals.Call +">APRS,TCPIP:=" + Globals.Pos[0] + "/" + Globals.Pos[1] + "& " + Globals.Info
	Globals.AprsStat = "Not active"

def sendMsg( msg ) :
	if (Globals.Active.lower() in ['true', '1', 'yes'] ) :
		AIS = aprslib.IS(Globals.Call, Globals.Passcode, port=14580)
		AIS.connect()
		AIS.sendall(msg)
		AIS.close()
		Globals.AprsStat = "Active"
	else :
		logger.info("APRS-IS: %s" % Globals.Active)
		Globals.AprsStat = "Test"
	Globals.LastPkt = msg
	logger.info("APRS Packet sent: %s" % msg)


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

