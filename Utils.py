#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul  Utils
- logEvent: Log Events with timstamp into global Log-List
"""

import pdb
from datetime import datetime
import re
import urllib.request
import socket
import time
import Config

LastHeard= []

def logRX(stn) :
	global LastHeard
	LastHeard.append(datestring() + ": " + stn)
	if len(LastHeard) > 99 :
		LastHeard = LastHeard[1:]

def logEvent(event) :
	f = open(Config.Logfile, "a")
	f.write(datestring() + ": " + event + "\n")
	f.close()

def match(strg, search=re.compile(r'[^A-Z0-9.-]').search):
	"""
	Test auf ungültige Zeichen
	"""
	res = bool(search(strg))
	return(True)

def grad2min(_lat, _lon) :
	"""
	Umrechnen von Dezimal-Grad zu Grad-Minuten
	"""
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

def datestring() :
        now = datetime.now()
        return (now.strftime('%Y-%m-%d %H:%M:%S'))

def elapsedTime() :
	end_time = time.time()
	tmp = end_time - Config.StartTime
	_d = tmp //84600
	tmp = tmp - 84600 * _d
	_h = tmp//3600
	tmp = tmp - 3600 * _h
	_m = tmp //60
	_s = tmp - 60 * _m
	return("%dd %dh %dm %ds" %(_d, _h,_m,_s))

def checkInternet() :
	logEvent("No Internet")
	HMI.display(4)
	time.sleep(5)

def connect():
	try:
		urllib.request.urlopen('http://google.com') #Python 3.x
		return True
	except:
		return False

def getip():
	st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		st.connect(('10.255.255.255', 1))
		_ip = st.getsockname()[0]
	except Exception:
		#pdb.set_trace()
		_ip = '127.0.0.1'
	finally:
		st.close()
	return(_ip)

def main() :
	logEvent("Startup")
	pdb.set_trace()
	print(logList)



if __name__ == "__main__":
        main()





