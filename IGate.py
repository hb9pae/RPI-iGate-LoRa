#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul  iGate
- main() Module
- lädt HMI.py und LoRa-RX Module
"""


import pdb
import logging
import LoraRx		# LoRa empfänger
import HMI		# Display und Tasten
import Config
import APRS
import BME280
import time
from threading import Timer
from datetime import timezone
import datetime

"""
__version__     = "0.0.3"
__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2023"
__email__       = "hb9pae@gmail.com"


Version = __version__
myConfig = "./igate.ini"

RxCount = 0

Frequ   = 433775000
SR      = 12

StartTime = datetime.datetime.now()
DisplayTimeout = 60

Temperature = 1.0
AirPressureNN = 1.0
Humidity = 1.0

LastMsg = "--- None ---"
PktErr = 0
PktSent = 0

LastPktRRSI = 0
CurrtRRSI = 0
SNR = 0
"""

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

def sendBeacon(_txt) :
	BeaconTxt = Config.CALL +">APRS,TCPIP:=" + Config.POS[0] + "/" + Config.POS[1] + "& " + Config.INFO + _txt
	APRS.sendMsg(BeaconTxt)

def sendWx(_txt) :

	try :
		_altitude = int(Config.HEIGHT)
	except:
		logging.basicConfig(level=logging.info, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
		logger = logging.getLogger(__name__)
		logger.info("Wrong Height format")
		_altitude = 400
 
	(temp, press_nn, hum) = BME280.getBME280(_altitude)
	Config.Temperature = temp
	Config.AirPressureNN = press_nn
	Config.Humidity = hum
	_tempf = (temp * 1.8) + 32 # APRS benötigt Farenheit 
	#pdb.set_trace()

	dt = datetime.datetime.now(timezone.utc)
	_DHM = dt.strftime("@%d%H%Mz")
	_pos = Config.POS[0] + "/" + Config.POS[1] 
	_wind  = "_.../...g..."
	_temp = "t" + str(int(round(_tempf,1)))
	_rain = "r...p...P..."
	_hum = "h" + str(int(round(hum)))
	_press = "b" + str(int(10*round(press_nn,1)))
	_id = " BME280"

	WxReport = Config.CALL + ">APRS:" +_DHM + _pos + _wind + _temp + _rain + _hum + _press  + _id
	APRS.sendMsg(WxReport)

def elapsedTime() :
	end_time = time.time()
	tmp = end_time - Config.StartTime
	_h = tmp//3600
	tmp = tmp - 3600 * _h
	_m = tmp //60
	_s = tmp - 60 * _m
	print("Elapsed Time: %dh %dm %ds" %(_h,_m,_s))

def init() :
	Config.StartTime = time.time()
	myconf = Config.getConfig(Config.myConfig)
	Config.setGlobals(myconf)
	APRS.init()
	Config.IP = HMI.getip()
	HMI.initbutton()
	LoraRx.init()

def main() :
	logging.basicConfig(level=logging.info, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
	logger = logging.getLogger(__name__)

	sendBeacon(" Start")
	bcTimer = RepeatedTimer(int(Config.BEACONINTERVAL), sendBeacon, " " + str(Config.RxCount) ) 

	#pdb.set_trace()

	if (Config.BME280.lower() in ['true', '1', 'yes'] ) :
		wxTimer = RepeatedTimer(int(Config.WXINTERVAL), sendWx, "") 
		logger.info("BME280 detected")

	try:
		while(1) :
			msg=LoraRx.loralib.recv()
			if msg[5] == 0 and msg[1] > 0:
				LoraRx.gotPacket(msg)
			time.sleep(0.05) 

			if (Config.Menu < 5) :
				HMI.display(Config.Menu)
				Config.Menu = 99
			if (time.time() - Config.DisplayOn) > Config.DisplayTimeout :
				HMI.initdisplay()
				Config.DisplayOn += 99999999.9

	finally:
		bcTimer.stop() 
		wxTimer.stop() 
		HMI.initdisplay()



if __name__ == "__main__":
	init()
	main()








