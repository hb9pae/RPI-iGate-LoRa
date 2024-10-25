#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul Config.py
Enthält alle Globalen Variablen
"""

import configparser
import os
import pdb
import datetime
import Utils

__version__     = "1.2.2"
__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__       = "hb9pae@gmail.com"

Version = __version__
myConfig = os.path.dirname(os.path.abspath(__name__)) + "/igate.ini"
Logfile = "/var/log/iGate.log"
WXrrd = os.path.dirname(os.path.abspath(__name__)) + "/WXrrd.rrd"

Frequ   = 433775000
SR      = 12

StartTime = datetime.datetime.now()
DisplayTimeout = 60

# Auslesen BME280

Temperature = 1.0
AirPressureNN = 1.0
Humidity = 1.0
BMEInterval = 300


# LORA
LastRx = "--- None ---"
LastMsg = "--- None ---"
RxCount = 0
PktErr = 0
# Message to APRS-IS
MsgSent = 0
PktRSSI = 0
RSSI = 0
SNR = 0


# Variablen aus igate.ini ----
ConfigDict = {}
Section = "APRS-iGate"

dirtyFlag = False
reboot = False
loopmax=0

#APRS
AIS = ""
Login = 0

confHeader = ["# Konfiguration LoRa-APRS iGate\n",\
	"# Positionskoordinaten im Dezimalformat (LAT: Breitengrad,LON: Längengrad)\n", \
	"# Höhenangaben im Meter über NN\n" ]

defConf = {
	"Call": "NOCALL", "Passcode" : "123456", "EN_APRSIS" : "False",\
	"Lat" : "47.5", "Lon" : "8.5", "height" : "399",\
	"BeaconInterval" : "900", "BeaconMsg": "LoRa iGate SWISS-ARTG", "EN_BME280" : "False",\
	"EN_WxData" : "False", "WebIP" : "0.0.0.0"
	}

def initConfigDict(_config) :
	ConfigDict.clear()
	for Section in _config :
		for key in _config[Section] :
			varname =  _config[Section][key]
			if (key.lower() == "call" ):
				varname = varname.upper()
			if (key.lower().startswith("en_") ):
				#pdb.set_trace()
				if (varname.lower() in [ "true", "1", "y", "yes"] ) :
					varname = True
				else :
					varname = False
			ConfigDict[key] = varname

		ConfigDict["pos"] = Utils.grad2min(float(ConfigDict["lat"]), float(ConfigDict["lon"]) )
		#pdb.set_trace()

def getConfig() :
	if  (not os.path.isfile(myConfig)) :
		wrConfig(defConf)  # write default configuration
		Utils.logEvent("No Configfile found, create %s" % (myConfig) )

	config = configparser.ConfigParser()
	config.read(myConfig)
	dictionary = {}
	for _section in config.sections():
		dictionary[_section] = {}
		for option in config.options(_section):
			dictionary[_section][option] = config.get(_section, option)
	return(dictionary)

def wrConfig(newconfig) :
	now = datetime.datetime.now()
	f = open(myConfig, "w")
	f.writelines(confHeader)
	f.writelines(now.strftime("# Erstellt: %d.%m.%Y %H:%M:%S\n") )
	f.writelines("# (c) hb9pae@gmail.com\n# -----\n")
	f.close()

	# ---- Write Configuration Template 
	_conf=configparser.ConfigParser()
	_conf[Section] = newconfig

	with open(myConfig, 'a') as configfile:
		_conf.write(configfile)


def main() :
	pdb.set_trace()



if __name__ == "__main__":
        main()





