#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul  iGate
- main() Modul
"""
__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__ = "hb9pae@gmail.com"

import LoraRx		# LoRa empfänger
import Config
import APRS
import WX
import Button
import Display
import App

import os, sys
import pdb
import logging
import time
import threading
from signal import SIGKILL
from threading import Timer
from datetime import timezone
import datetime
import warnings
import subprocess
#import RPi.GPIO as GPIO
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

def checkInternet() :
	n = 1
	while not connect() :
		logging.info("No Internet")
		Display.display(4)
		time.sleep(n)
		n = n*2

def connect():
	try:
		urllib.request.urlopen('http://google.com') #Python 3.x
		return True
	except:
		return False

def init() :
	# wird in Config gesetzt 	Config.StartTime = time.time()
	myconf = Config.getConfig(Config.myConfig)
	Config.setGlobals(myconf)
	checkInternet()
	Config.IP = Button.getip() 
	#pdb.set_trace()
	Display.init()
	Button.init()
	APRS.init()
	LoraRx.init()
	WX.readBME280()

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

	webgui = threading.Thread(target=App.run, args=(Config.WEBIP,))
	webgui.start()
	logging.info("IGate init done, Webinterface http://:%s:5000", Config.WEBIP)

	# Send StartBeacon
	sendBeacon()

def main() :
	warnings.filterwarnings("ignore", category=DeprecationWarning)
	logging.basicConfig(filename='/var/log/iGate.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	logging.info("IGate started")

	init()
	#Display.display(0)

	while(True) :
		LoraRx.loraRX()
		#print("Menue: %d, Last: %d" % (Config.Menu, Config.MenuLast) )

		if (Config.Menu < 10) :
			Display.display(Config.Menu)

		to = int(time.time() - Config.DisplayOn) 
		if to > Config.DisplayTimeout :
			Display.clear()
			#pdb.set_trace()
			Config.DisplayOn += 99999999.9

		if (Config.reboot) :
			Config.reboot = False
			pid = os.getpid()
			os.kill(pid, SIGKILL)
		if (Config.ReadBME280) :
			Config.ReadBME280 = False
			WX.BMEInterval()
		if (Config.WxReport) :
			Config.WxReport = False
			WX.WxReport()
		if (Config.Beacon) :
			Config.Beacon = False
			sendBeacon()

		time.sleep(0.05) 

if __name__ == "__main__":
	main()



