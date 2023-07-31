#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul Config.py
Enthält alle Globalen Variablen
"""

import configparser
import os
import pdb
import logging
import re
import datetime


__version__     = "0.0.5"
__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2023"
__email__       = "hb9pae@gmail.com"

Version = __version__
myConfig = os.path.dirname(os.path.abspath(__name__)) + "/igate.ini"
Frequ   = 433775000
SR      = 12

StartTime = datetime.datetime.now()
DisplayTimeout = 60

# Auslesen BME280
EN_WXDATA = False
BMEINTERVAL = 300
WXINTERVAL = 300
Temperature = 1.0
AirPressureNN = 1.0
Humidity = 1.0

# LORA
LastMsg = "--- None ---"
RxCount = 0
PktErr = 0
# Message to APRS-IS
MsgSent = 0
PktRSSI = 0
RSSI = 0
SNR = 0


# Variablen aus igate.ini ----
CALL = "NOCALL"
PASSCODE = ""
INFO = "" 
EN_APRSIS = False
LON = 0.0
LAT = 0.0
HEIGHT = 0
BEACONINTERVAL = 600
BEACONMESSAGE = "-"
EN_BME280 = False

dirtyFlag = False
reboot = False

# Test auf ungültige Zeichen
def match(strg, search=re.compile(r'[^A-Z0-9.-]').search):
	res = bool(search(strg))
	return(True)

# Umrechnen von Dezimal-Grad zu Grad-Minuten
def grad2min(_lat, _lon) :
	_latGrad = int(abs(_lat))
	_latMin = 60* (_lat - _latGrad)
	latstr = f"{_latGrad:d}{_latMin:.2f}"
	if (_lat > 0) :
		latstr = latstr.zfill(7) + "N"
	else :
		latstr = latstr + "S"

	_lonGrad = int(abs(_lon))
	_lonMin = 60.0 * (_lon - _lonGrad)
	lonstr = f"{_lonGrad:d}{_lonMin:.2f}"
	if (_lon > 0) :
		lonstr = lonstr.zfill(8) + "E"
	else :
		lonstr = lonstr + "W"

	return(latstr, lonstr)

def setGlobals(_conf) :
	global POS

	#pdb.set_trace()
	for section in _conf :
		for key in _conf[section] :
			varname =  _conf[section][key]
			#pdb.set_trace()
			if (key.lower().startswith("en_") ):
				if (varname.lower() in [ "true", "1", "y", "yes"] ) :
					varname = True
				else :
					varname = False
			globals()[key.upper()] = varname
		POS = grad2min(float(LAT), float(LON) )

def getConfig(file) :
	if (os.path.isfile(file)) :
		config = configparser.ConfigParser()
		config.read(file)
		dictionary = {}
		for section in config.sections():
			dictionary[section] = {}
			for option in config.options(section):
				dictionary[section][option] = config.get(section, option)
		return(dictionary)
	else :
		mkConfig(file)
		print("No Configfile found, create %s and exit Program" % (file) )
		exit(1)

def mkConfig(file) :
		logging.info("No Configfile found, create %s and exit Program" % (file))

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
		_conf["APRS-IS"] = {
			"Call": "NOCALL", "Passcode" : "123456", "Info" : "LoRa iGate", "EN_APRSIS" : "False",\
			"Lat" : "47.53668", "Lon" : "8.58164", "height" : "399",\
			"BeaconInterval" : "600", "BeaconMessage" : "-", "EN_BME280" : "False",\
			"EN_WxData" : "False", "WxInterval" : "300"
			}
		with open(file, 'a') as configfile:
			_conf.write(configfile)
		

def main() :
	myconf = getConfig("test.ini")
	setGlobals(myconf)
	pdb.set_trace()



if __name__ == "__main__":
        main()





