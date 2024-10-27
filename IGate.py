#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul  iGate
- main() Module
- lädt HMI.py und LoRa-RX Module
V 1.2.2 vom 2024-10-22
V 1.2.1 vom 2024-10-07
"""

import os, sys, signal
import pdb
import Utils
import LoraRx		# LoRa empfänger
import HMI		# Display und Tasten
import Config
import APRS
import App
import WX
import time
import threading
from threading import Timer
from datetime import timezone
import datetime
import warnings
import subprocess
import RPi.GPIO as GPIO

class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer     = None
		self.interval   = interval
		self.function   = function
		self.args       = args
		self.kwargs     = kwargs
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
		self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False

def sendBeacon() :
	BeaconTxt = Config.ConfigDict["call"] +">APRS,TCPIP:=" + Config.ConfigDict["pos"][0] + "L" + Config.ConfigDict["pos"][1] + "&PHG0000 " + Config.ConfigDict["beaconmsg"] 
	APRS.sendMsg(BeaconTxt)

def init() :
	Config.StartTime = time.time()
	Config.initConfigDict(Config.getConfig())
	#checkInternet()
	Config.ConfigDict["webip"] = Utils.getip()
	APRS.init()
	HMI.initbutton()
	LoraRx.init()
	#WX.readBME280()
	#pdb.set_trace()

	# Init Timer	iGate-Beacon, BME280, WX-Beacon
	iGateTimer = RepeatedTimer(int(Config.ConfigDict["beaconinterval"]), sendBeacon ) 
	iGateTimer.start()
	Utils.logEvent("Beacon Timer started Interval %s sec." % (Config.ConfigDict["beaconinterval"]) )

	if (Config.ConfigDict["en_bme280"]) :
		BMETimer = RepeatedTimer(int(Config.BMEInterval), WX.BMEInterval ) 
		BMETimer.start() 
		Utils.logEvent("BME280 Timer started Interval %s sec." % (Config.ConfigDict["bmeinterval"]) )

		WxTimer = RepeatedTimer(int(Config.ConfigDiConfig.ConfigDict["wxinterval"] ), WX.WxReport ) 
		WxTimer.start()
		Utils.logEvent("Wx Timer started Interval %s sec." % (Config.ConfigDict["wxinterval"]) )

	webgui = threading.Thread(target=App.run, args=(Config.ConfigDict["webip"],))
	webgui.start()
	Utils.logEvent("LoRa APRS iGate init done, Webinterface %s:5000" % (Config.ConfigDict["webip"]) )

	# Send StartBeacon
	sendBeacon()
	#pdb.set_trace()

def extCmd() :
	while True :
		if (Config.Menu < 5) :
			HMI.display(Config.Menu)
			Config.Menu = 99
		if (time.time() - Config.DisplayOn) > Config.DisplayTimeout :
			HMI.initdisplay()
			Config.DisplayOn += 99999999.9
		if (Config.reboot) :
			Config.reboot = False
			pid = os.getpid()
			os.kill(pid, signal.SIGTERM)

		time.sleep(0.5) 


def main() :
	warnings.filterwarnings("ignore", category=DeprecationWarning)
	Utils.logEvent("IGate started, V %s" % (Config.Version) )

	init()
	#pdb.set_trace()
	t_extcmd = threading.Thread(target=extCmd, args=())
	t_extcmd.start()

	loopcnt = 0		#Verzögere die Abarbeitung Display und Button Funktionen
	Config.loopmax = [ ]
	loopstart = time.time()
	while(True) :
		loopcnt +=1
		LoraRx.LoraRx()
		time.sleep(0.01)
		if loopcnt > 1000 :
			Config.loopmax.append( int ((time.time() - loopstart )) ) 
			loopcnt = 0
			loopstart = time.time() 
			if len(Config.loopmax) > 9 :
				Config.loopmax = Config.loopmax[1:]

if __name__ == "__main__":
	main()



