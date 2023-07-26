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
import threading
from threading import Timer
from datetime import timezone
import datetime
import app
import warnings


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
	BeaconTxt = Config.CALL +">APRS,TCPIP:=" + Config.POS[0] + "L" + Config.POS[1] + "&PHG0000 " + Config.INFO + " " + str(Config.RxCount) 
	APRS.sendMsg(BeaconTxt)

def sendWx(_txt) :
	if (Config.BME280.lower() in ['true', '1', 'yes'] ) :
		try :
			_altitude = int(Config.HEIGHT)
		except:
			logging.info("Wrong Height format")
			_altitude = 400
		try :
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
		except :
			Config.BME280="False"
			logging.info("BME280 not available, disable WX-Timer")

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
	Config.dirtyFlag = False
	logging.info("IGate init done")

def main() :
	sendBeacon()
	#bcTimer = RepeatedTimer(int(Config.BEACONINTERVAL), sendBeacon, " " + str(Config.RxCount) ) 
	bcTimer = RepeatedTimer(int(Config.BEACONINTERVAL), sendBeacon ) 
	bcTimer.start()

	#webgui = threading.Thread(target=app.run, args=("127.0.0.1",))
	webgui = threading.Thread(target=app.run, args=("0.0.0.0",))
	webgui.start()

	if (Config.BME280.lower() in ['true', '1', 'yes'] ) :
		wxTimer = RepeatedTimer(int(Config.WXINTERVAL), sendWx, "")
		wxTimer.start() 
		logging.info("BME280 detected, Timer started")

	while(True) :
		msg=LoraRx.loralib.recv()
		if msg[1] > 0 and msg[5] > 1:
			PktErr += 1
			logging.info("Packet received, CRC Error")
		if msg[5] == 0 and msg[1] > 0:
			#pdb.set_trace()
			LoraRx.gotPacket(msg)
			HMI.display(3)  # display received Packaage
		time.sleep(0.05) 

		if (Config.Menu < 5) :
			HMI.display(Config.Menu)
			Config.Menu = 99
		if (time.time() - Config.DisplayOn) > Config.DisplayTimeout :
			HMI.initdisplay()
			Config.DisplayOn += 99999999.9
		if  (Config.dirtyFlag) :
			logging.info("Configuration reloaded")
			Config.dirtyFlag = False


	bcTimer.stop()
	HMI.initdisplay()


if __name__ == "__main__":
	warnings.filterwarnings("ignore", category=DeprecationWarning)
	#logging.basicConfig(filename="/var/log/iGate.log", level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
	logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
	logging.info("IGate startup")
	init()
	main()








