#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import aprslib
import Config
import Utils
import pdb

def init() :
	Config.AprsStat = "Not active"
	Config.Login = 0
	if (Config.ConfigDict["en_aprsis"] ) :
		try :
			Config.AIS = aprslib.IS(Config.ConfigDict["call"], Config.ConfigDict["passcode"], port=14580)
			Config.AIS.connect()
			Config.Login += 1
		except: 
			Utils.logEvent("APRS-IS upload failed")

def sendMsg( msg ) :
	Utils.logRX("APRS Packet to send: %s" %  msg)
	if (Config.ConfigDict["en_aprsis"]) :
		#pdb.set_trace()
		if not Config.AIS._connected  :
			Config.AIS = aprslib.IS(Config.ConfigDict["call"], Config.ConfigDict["passcode"] , port=14580)
			Config.AIS.connect()
			Config.Login += 1
		try :
			Config.AIS.sendall(msg)
			Config.AprsStat = "Active"
			Config.MsgSent +=1
		except: 
			Utils.logEvent("APRS-IS upload failed")

	else :
		Config.AprsStat = "Test"

	Config.LastPkt = msg



