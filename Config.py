
import configparser
import os
import pdb
import logging
import re

import Globals

# Test auf ungültige Zeichen
def match(strg, search=re.compile(r'[^A-Z0-9.-]').search):
	res = bool(search(strg))
	return(True)

# Umrechnen von Dezimal-Grad zu Grad-Minuten
def grad2min(_lat, _lon) :
	_lonGrad = int(abs(_lon))
	_lonMin = 60.0 * (_lon - _lonGrad)
	lonstr = f"{_lonGrad:d}{_lonMin:.2f}"
	if (_lon > 0) :
		lonstr = lonstr.zfill(8) + "E"
	else :
		lonstr = lonstr + "W"
	_latGrad = int(abs(_lat))
	_latMin = 60* (_lat - _latGrad)
	latstr = f"{_latGrad:d}{_latMin:.2f}"
	if (_lat > 0) :
		latstr = latstr.zfill(7) + "N"
	else :
		latstr = latstr + "S"
	return(latstr, lonstr)

def readConfig(file) :
	if (os.path.isfile(file)) :
		cp=configparser.ConfigParser()

		cp.read(file)
		Globals.Call = cp.get("APRS-IS","Call").upper()
		Globals.Passcode = cp.get("APRS-IS", "Passcode")
		Globals.Info = cp.get("APRS-IS","Info")
		Globals.Active = cp.get("APRS-IS","Active")
		
		Globals.Lat = float(cp.get("Position","Lat"))
		Globals.Lon = float(cp.get("Position","Lon"))
		Globals.Pos = grad2min(Globals.Lon, Globals.Lat)
		Globals.Alt = int(cp.get("Position", "Height"))

		Globals.BeaconInterval = int(cp.get("Beacons","BeaconInterval") )
		Globals.BeaconMessage  = cp.get("Beacons", "BeaconMessage")

		Globals.BME280 = bool(cp.get("WX","BME280"))
		Globals.WxInterval = int(cp.get("WX","WxInterval") )
		#pdb.set_trace()
	else :
		print("No Configfile, create new one")

		config=configparser.ConfigParser()
		config["APRS-IS"] = {"Call": "NOCALL", "Passcode" : "123456", "Info" : "LoRa iGate", "Active" : False}
		config["Position"] = {"Lon" : "47.53668", "Lat" : "8.58164", "Height" : "399"}
		config["Beacons"] = {"BeaconInterval" : "300", "BeaconMessage" : "-"}
		config["WX"] = {"BME280" : "True", "WxInterval" : "300"}
		with open(file, 'w') as configfile:
			config.write(configfile)
		print("Done")
		exit(1)



#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
#logger = logging.getLogger(__name__)




