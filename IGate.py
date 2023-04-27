#! /usr/bin/python3elp
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

import Globals


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
	BeaconTxt = Globals.Call +">APRS,TCPIP:=" + Globals.Pos[0] + "/" + Globals.Pos[1] + "& " + Globals.Info + _txt
	APRS.sendMsg(BeaconTxt)

def sendWx(_txt) :
	(temp, press_nn, hum) = BME280.getBME280(Globals.Alt)
	Globals.Temperature = temp
	Globals.AirPressureNN = press_nn
	Globals.Humidity = hum
	_tempf = (temp * 1.8) + 32 # APRS benötigt Farenheit 
	#pdb.set_trace()

	dt = datetime.datetime.now(timezone.utc)
	_DHM = dt.strftime("@%d%H%Mz")
	#_pos = str(Globals.Lat) + "/" + str(Globals.Lon) 
	_pos = Globals.Pos[0] + "/" + Globals.Pos[1] 
	_wind  = "_.../...g..."
	_temp = "t" + str(int(round(_tempf,1)))
	_rain = "r...p...P..."
	_hum = "h" + str(int(round(hum)))
	_press = "b" + str(int(10*round(press_nn,1)))
	_id = " BME280"

	WxReport = Globals.Call + ">APRS:" +_DHM + _pos + _wind + _temp + _rain + _hum + _press  + _id
	APRS.sendMsg(WxReport)

def elapsedTime() :
	end_time = time.time()
	tmp = end_time - Globals.StartTime
	_h = tmp//3600
	tmp = tmp - 3600 * _h
	_m = tmp //60
	_s = tmp - 60 * _m
	print("Elapsed Time: %dh %dm %ds" %(_h,_m,_s))

def init() :
	Globals.StartTime = time.time()
	pass

def main() :
	logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
	logger = logging.getLogger(__name__)

	Config.readConfig(Globals.myConfig)
	APRS.init()
	sendBeacon(" Start")
	bcTimer = RepeatedTimer(Globals.BeaconInterval, sendBeacon, str(Globals.RxCount) ) 
	if (Globals.BME280) :
		wxTimer = RepeatedTimer(Globals.WxInterval, sendWx, "") 
		logger.info("BME280 detected %s", Globals.BME280)
	#pdb.set_trace()

	Globals.IP = HMI.getip()
	HMI.initbutton()
	LoraRx.init()

	try:
		while(1) :
			msg=LoraRx.loralib.recv()
			if msg[5] == 0 and msg[1] > 0:
				LoraRx.gotPacket(msg)
			time.sleep(0.05) # your long-running job goes here...

			if (Globals.Menu < 5) :
				HMI.display(Globals.Menu)
				Globals.Menu = 99
			if (time.time() - Globals.DisplayOn) > Globals.DisplayTimeout :
				HMI.initdisplay()
				Globals.DisplayOn += 99999999.9

	finally:
		bcTimer.stop() 
		wxTimer.stop() 
		HMI.initdisplay()



if __name__ == "__main__":
	init()
	main()








