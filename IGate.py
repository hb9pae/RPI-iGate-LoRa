#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul  iGate
- main() Module
- lädt HMI.py und LoRa-RX Module
V 1.2.1 vom 2024-10-07
"""

import os, sys, signal
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
import urllib.request

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
	BeaconTxt = Config.CALL +">APRS,TCPIP:=" + Config.POS[0] + "L" + Config.POS[1] + "&PHG0000 " + Config.INFO  
	APRS.sendMsg(BeaconTxt)

def aelapsedTime() :
	end_time = time.time()
	tmp = end_time - Config.StartTime
	_h = tmp//3600
	tmp = tmp - 3600 * _h
	_m = tmp //60
	_s = tmp - 60 * _m
	return("%dh %dm %ds" %(_h,_m,_s))

def checkInternet() :
	logging.info("No Internet")
	HMI.display(4)
	time.sleep(5)

def connect():
	try:
		urllib.request.urlopen('http://google.com') #Python 3.x
		return True
	except:
		return False

def init() :
	Config.StartTime = time.time()
	myconf = Config.getConfig(Config.myConfig)
	Config.setGlobals(myconf)
	#checkInternet()
	Config.IP = HMI.getip() 
	#pdb.set_trace()
	APRS.init()
	#Config.IP = HMI.getip()
	HMI.initbutton()
	LoraRx.init()
	#WX.readBME280()

	# Init Timer	iGate-Beacon, BME280, WX-Beacon
	iGateTimer = RepeatedTimer(int(Config.BEACONINTERVAL), sendBeacon ) 
	iGateTimer.start()
	logging.info("Beacon Timer started Interval %s sec.", Config.BEACONINTERVAL )

	if (Config.EN_BME280) :
		BMETimer = RepeatedTimer(int(Config.BMEINTERVAL), WX.readBME280 ) 
		BMETimer.start() 
		logging.info("BME280 Timer started Interval %s sec.", Config.BMEINTERVAL )

		WxTimer = RepeatedTimer(int(Config.WXINTERVAL), WX.WxReport ) 
		WxTimer.start()
		logging.info("Wx Timer started Interval %s sec.", Config.WXINTERVAL )

	webgui = threading.Thread(target=app.run, args=(Config.WEBIP,))
	webgui.start()
	logging.info("IGate init done, Webinterface <RPI-IP>:5000")

	# Send StartBeacon
	sendBeacon()

def main() :
	warnings.filterwarnings("ignore", category=DeprecationWarning)
	logging.basicConfig(filename='/var/log/iGate.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	logging.info("IGate started, V %s ", Config.Version)

	init()
	print("BME %s", Config.BMEINTERVAL)
	while(True) :
		msg=LoraRx.loralib.recv()
		if msg[1] > 0 and msg[5] > 1:
			PktErr += 1
			logging.info("Packet received, CRC Errors: %d", PktErr)
			logging.info("Packet Size [0] %d, CRC [5] %d", msg[1], msg[5])
		if msg[1] > 0 and msg[5] == 0 :
			logging.info("Packet received, no CRC error")
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
			Config.reboot = False
			pid = os.getpid()
			os.kill(pid, signal.SIGTERM)


if __name__ == "__main__":
	main()



