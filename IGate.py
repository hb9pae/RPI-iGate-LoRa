#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul  iGate
- main() Module
- lädt HMI.py und LoRa-RX Module
"""

import os, sys
import pdb
import logging
import LoraRx		# LoRa empfänger
import HMI		# Display und Tasten
import Config
import APRS
import WX
import time
import threading
from threading import Timer
from datetime import timezone
import datetime
import app
import warnings
import subprocess
import RPi.GPIO as GPIO

myLog = os.path.dirname(os.path.abspath(__name__)) + "/iGate.log"

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
	logging.info("Send iGate Beacon")
	BeaconTxt = Config.CALL +">APRS,TCPIP:=" + Config.POS[0] + "L" + Config.POS[1] + "&PHG0000 " + Config.INFO + " " + str(Config.RxCount) 
	APRS.sendMsg(BeaconTxt)

def igateBeacon() :
	Config.Beacon = True

def readBME280() :
	Config.ReadBME280 = True

def WxReport() :
	Config.WxReport = True

def aelapsedTime() :
	end_time = time.time()
	tmp = end_time - Config.StartTime
	_h = tmp//3600
	tmp = tmp - 3600 * _h
	_m = tmp //60
	_s = tmp - 60 * _m
	return("%dh %dm %ds" %(_h,_m,_s))

def init() :
	Config.StartTime = time.time()
	myconf = Config.getConfig(Config.myConfig)
	Config.setGlobals(myconf)
	APRS.init()
	Config.IP = HMI.getip()
	HMI.initbutton()
	LoraRx.init()
	WX.readBME280()
	#pdb.set_trace()

	# Init Timer	iGate-Beacon, BME280, WX-Beacon
	iGateTimer = RepeatedTimer(int(Config.BEACONINTERVAL), igateBeacon ) 
	iGateTimer.start()
	logging.info("Beacon Timer started Interval %s sec.", Config.BEACONINTERVAL )

	if (Config.EN_BME280) :
		BMETimer = RepeatedTimer(int(Config.BMEINTERVAL), readBME280 ) 
		BMETimer.start() 
		logging.info("BME280 Timer started Interval %s sec.", Config.BMEINTERVAL )

		WxTimer = RepeatedTimer(int(Config.WXINTERVAL), WxReport ) 
		WxTimer.start()
		logging.info("Wx Timer started Interval %s sec.", Config.WXINTERVAL )

	webgui = threading.Thread(target=app.run, args=("0.0.0.0",))
	webgui.start()
	logging.info("IGate init done")

	# Send StartBeacon
	sendBeacon()

def main() :
	warnings.filterwarnings("ignore", category=DeprecationWarning)
	logging.basicConfig(filename='/var/log/iGate.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	logging.info("IGate startup")

	init()
	while(True) :
		msg=LoraRx.loralib.recv()
		if msg[1] > 0 and msg[5] > 1:
			PktErr += 1
			logging.info("Packet received, CRC Error")
		if msg[5] == 0 and msg[1] > 0:
			#pdb.set_trace()
			LoraRx.gotPacket(msg)
			HMI.display(3)  # display received Packaage
		time.sleep(0.1) 

		if (Config.Menu < 5) :
			HMI.display(Config.Menu)
			Config.Menu = 99
		if (time.time() - Config.DisplayOn) > Config.DisplayTimeout :
			HMI.initdisplay()
			Config.DisplayOn += 99999999.9
		if (Config.reboot) :
			os.system('sudo reboot')
		if (Config.ReadBME280) :
			Config.ReadBME280 = False
			WX.BMEInterval()
		if (Config.WxReport) :
			Config.WxReport = False
			WX.WxReport()
		if (Config.Beacon) :
			Config.Beacon = False
			sendBeacon()

	HMI.initdisplay()
	GPIO.cleanup()
	main()

if __name__ == "__main__":
	main()



