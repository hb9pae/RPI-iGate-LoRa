
from  flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_basicauth import BasicAuth
import time
import pdb
import configparser, json
import Config
import IGate
import threading
import subprocess 
import os, sys
from datetime import datetime

from flask.logging import default_handler
import logging


__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__ = "hb9pae@gmail.com"

myconf = Config.getConfig(Config.myConfig)


App = Flask(__name__)
App.logger.removeHandler(default_handler)

App.config['BASIC_AUTH_USERNAME'] = myconf.get("APRS").get("call")
App.config['BASIC_AUTH_PASSWORD'] = myconf.get("APRS").get("secret")

basic_auth = BasicAuth(App)


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def isdirty() :
	if Config.dirtyFlag :
		_dirty = "True"
	else :
		_dirty = "False"
	return(_dirty)

def datestring() :
	now = datetime.now()
	return (now.strftime('%Y-%m-%d %H:%M:%S'))

def run(ip) :
	 App.run(ip, debug=False)

def elapsedTime() :
	end_time = time.time()
	tmp = end_time - Config.StartTime
	_h = tmp//3600
	tmp = tmp - 3600 * _h
	_m = tmp //60
	_s = tmp - 60 * _m
	return("%dh %dm %ds" %(_h,_m,_s))

def saveconfig(newconf) :
	header1 = "# Konfiguration APRS iGate\n"
	header2 = "# (c) hb9pae@gmail.com\n"
	header3 = "# Positionskoordinaten im Dezimalformat (LAT: Breitengrad,LON: Laengengrad)\n" 
	header4 = "# " + datestring() + "\n"
	f = open(Config.myConfig, "w")
	f.writelines(header1)
	f.writelines(header2)
	f.writelines(header3)
	f.writelines(header4)
	f.close()

	#pdb.set_trace()
	config = configparser.ConfigParser()
	config["APRS"] = newconf
	with open(Config.myConfig, "a") as configfile :
		config.write(configfile)

@App.route("/log/",  methods=['GET', 'POST'] )
def log() :
	myLog =  "/var/log/iGate.log"
	cmd = ("tail", "-100", myLog)
	res = subprocess.run(cmd, capture_output=True, text=True)
	out = res.stdout.split("\n")
	#pdb.set_trace()
	return render_template("log.html", content = out, ds = datestring(), dirty=isdirty())

@App.route("/debug/",  methods=['GET', 'POST'] )
# set breakpoint
def debug() :
	pdb.set_trace()


@App.route("/re_start")
def re_start() :
	# get the pid of the current process
	Config.reboot = True
	Config.dirtyFlag = 0
	return redirect(url_for('status') )

@App.route("/config/",  methods=['GET', 'POST'] )
@basic_auth.required
def config() :
	myconfig = Config.getConfig(Config.myConfig)
	#pdb.set_trace()

	configlist={}
	for section in myconfig :
	        for key in myconfig[section] :
                	configlist.update({key:myconfig[section][key]})

	if request.method == "POST" :
		myconfig = request.form.to_dict()
		#pdb.set_trace()
		saveconfig(myconfig)

		myconf = Config.getConfig(Config.myConfig)
		Config.setGlobals(myconf)
		#pdb.set_trace()
		Config.dirtyFlag = True
		return redirect(url_for('status') )
	return render_template("config.html", content = configlist, ds = datestring(), dirty = isdirty() )

@App.route('/')
def status() :
	#pdb.set_trace()
	to = (time.time() - Config.DisplayOn) 
	varlist={"Version" : Config.Version, "Rufzeichen":Config.CALL, "Status APRS-IS":Config.EN_APRSIS, "- Loginversuche":Config.Login," ":" ",
		"iGate LAT":Config.LAT, "iGate LON":Config.LON, "iGate Höhe":Config.HEIGHT, " " :" ",
		"Sensor BME280":Config.EN_BME280, "BME280 Intervall": Config.BMEINTERVAL, 
		"Temperatur":Config.Temperature, "Luftdruck":Config.AirPressureNN, "Luftfeuchtigkeit":Config.Humidity," ":" ",
		"Lezte Meldung":Config.LastMsg,"- Empfangen":Config.LastRx, "Signal RSSI": Config.RSSI, "Pkt RSSI": Config.PktRSSI, "SNR" : Config.SNR, 
		"Fehler": Config.RxErr, "APRS-IS Meldung": Config.MsgSent,"RX Zähler": Config.RxCount,
		"Wetter-Daten": Config.EN_WXDATA, "Wetter Intervall" : Config.WXINTERVAL,
		"Baken Intervall": Config.BEACONINTERVAL, "Baken Meldung": Config.BEACONMESSAGE, "Uptime": elapsedTime()
	}

	return render_template("status.html", content = varlist, ds = datestring(), dirty = isdirty())

@App.route('/about/')
def about() :
	#pdb.set_trace()
	return render_template('about.html', ds = datestring(), dirty = isdirty())

@App.route('/wx/')
def wx() :
	#pdb.set_trace()
	wxlist = [Config.Temperature, Config.Humidity, Config.AirPressureNN]
	if (Config.EN_WXDATA) :
		wx = "Show"
	else :
		wx = "Hide"
	return render_template('wx.html', content = wxlist, WxData = wx, ds = datestring(), dirty = isdirty())
	#pdb.set_trace()


if __name__ == '__main__':
	run("0.0.0.0")
