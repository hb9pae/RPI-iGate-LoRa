#! /usr/bin/python3Info

# -*- coding: utf-8 -*-

"""
Python Modul Config.py
Enthält alle Globalen Variablen
24-10-18: V 1.3.01  fast variante
24-11-03: V 1.3.02  Koordinatenumrechnung
24-11-20: V 1.3.02a SPI Clock neun 250000 Hz (LORA/lora.c)
"""

import configparser
import os
import pdb
import logging
import re
import datetime
import time
from math import floor


__version__     = "1.3.02"
__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__       = "hb9pae@gmail.com"

Version = __version__
myConfig = os.path.dirname(os.path.abspath(__name__)) + "/igate.ini"
Frequ   = 433775000
SR      = 12

StartTime = time.time()
Uptime = 0
DisplayOn = 0
DisplayTimeout = 60
Menu = 0
MenuLast = 0

# Auslesen BME280
EN_WXDATA = False
BMEINTERVAL = 300
WXINTERVAL = 300
Temperature = 1.0
AirPressureNN = 1.0
Humidity = 1.0
WXrrd = os.path.dirname(os.path.abspath(__name__)) + "/WXrrd.rrd"

ReadBME280 = False
WxReport = False
Beacon = False

# LORA RX
LastMsg = "None"
LastRx = "None"
PktSize = 0
PktRSSI = 0
RSSI = 0
SNR = 0
RxCount = 0
RxErr = 0
From = "None"
To = "None"

# Message to APRS-IS
MsgSent = 0


# Variablen aus igate.ini ----
CALL = "NOCALL"
PASSCODE = ""
EN_APRSIS = False
LON = 0.0
LAT = 0.0
HEIGHT = 0
BEACONINTERVAL = 600
BEACONMESSAGE = "-"
EN_BME280 = False
SECRET = ""

dirtyFlag = False
reboot = False

#APRS
AIS = ""
Login = 0

def upTime() :
	upt = time.time() - StartTime
	m, s = divmod(int(upt), 60)
	h, m = divmod(m, 60)
	return('{:02d}:{:02d}:{:02d}'.format(h, m, s))

def degrees_to_ddm(dd):
	degrees = int(floor(dd))
	minutes = (dd - degrees) * 60
	return (degrees, minutes)

def latitude_to_ddm(dd):
	direction = "S" if dd < 0 else "N"
	degrees, minutes = degrees_to_ddm(abs(dd))
	return "{0:02d}{1:05.2f}{2}".format(degrees, minutes, direction,)

def longitude_to_ddm(dd):
	direction = "W" if dd < 0 else "E"
	degrees, minutes = degrees_to_ddm(abs(dd))
	return "{0:03d}{1:05.2f}{2}".format(degrees, minutes, direction,)

# Umrechnen von Dezimal-Grad zu Grad-Minuten
#def grad2min(_lat, _lon) :
#	 return(latitude_to_ddm(_lat), longitude_to_ddm(_lon) )

def setGlobals(_conf) :
	global POS

	#pdb.set_trace()
	for section in _conf :
		for key in _conf[section] :
			varname =  _conf[section][key]
			if (key.lower().startswith("en_") ):
				#pdb.set_trace()
				if (varname.lower() in [ "true", "1", "y", "yes"] ) :
					varname = True
				else :
					varname = False
			if (key.lower() == "call" ):
				#pdb.set_trace()
					varname = varname.upper()

			globals()[key.upper()] = varname
		POS = latitude_to_ddm(float(LAT)), longitude_to_ddm(float(LON))

def getConfig(file) :
	#pdb.set_trace()
	if  (not os.path.isfile(file)) :
		mkConfig(file)
		logging.info("No Configfile found, create %s" % (file) )
		#os.system('sudo reboot')

	config = configparser.ConfigParser()
	config.read(file)
	dictionary = {}
	for section in config.sections():
		dictionary[section] = {}
		for option in config.options(section):
			dictionary[section][option] = config.get(section, option)
	return(dictionary)

def mkConfig(file) :
		# ---- Write Header to  Configfile 
		now = datetime.datetime.now() 
		header1 = "# Konfigurtation APRS iGate\n"
		header2 = "# (c) hb9pae@gmail.com\n"
		header3 = "# Positionskoordinaten im Dezimalformat (LAT: Breitengrad,LON: Laengengrad)\n" 
		header4 = now.strftime("# Erstellt: %d/%m/%Y %H:%M:%S\n")
		f = open(file, "w")
		f.writelines(header1)
		f.writelines(header2)
		f.writelines(header3)
		f.writelines(header4)
		f.close()

		# ---- Write Configuration Template 
		_conf=configparser.ConfigParser()
		_conf["APRS"] = {
			"Call": "NOCALL", "Passcode" : "123456", "EN_APRSIS" : "False",\
			"Lat" : "47.5", "Lon" : "8.5", "height" : "399",\
			"BeaconInterval" : "600", "BeaconMessage" : "LoRa iGate SWISS-ARTG", "EN_BME280" : "False",\
			"EN_WxData" : "False", "WxInterval" : "300", "SECRET" : "geheim", "WebIP" : "0.0.0.0"
			}
		with open(file, 'a') as configfile:
			_conf.write(configfile)
		

def main() :
	myconf = getConfig("test.ini")
	setGlobals(myconf)
	pdb.set_trace()



if __name__ == "__main__":
        main()





