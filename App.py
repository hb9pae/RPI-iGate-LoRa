
from  flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import time
import pdb
import configparser, json
import Config
import threading
import subprocess 
import os, sys
from datetime import datetime

from flask.logging import default_handler
import logging
import Utils

App = Flask(__name__)
App.logger.removeHandler(default_handler)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def isdirty() :
	if Config.dirtyFlag :
		_dirty = "True"
	else :
		_dirty = "False"
	return(_dirty)

def run(ip) :
	 App.run(ip, debug=False)

@App.route("/log/",  methods=['GET', 'POST'] )
def log() :
	cmd = ("tail", "-100", Config.Logfile)
	res = subprocess.run(cmd, capture_output=True, text=True)
	log = res.stdout.split("\n")
	#pdb.set_trace()
	#print(log)
	return render_template("log.html", content = log, ds = Utils.datestring(), dirty=isdirty())

@App.route("/stationen/",  methods=['GET', 'POST'] )
def stationen() :
	#pdb.set_trace()
	#print(Utils.logList) 
	return render_template("stationen.html", content = Utils.LastHeard, ds = Utils.datestring(), dirty=isdirty())

@App.route("/debug/",  methods=['GET', 'POST'] )
# set breakpoint
def debug() :
	pdb.set_trace()

@App.route("/reboot")
def reboot() :
	Config.reboot = True
	Config.dirtyFlag = False
	return redirect(url_for('status') )

@App.route("/config/",  methods=['GET', 'POST'] )
def config() :
	myconfig = Config.getConfig()

	configlist={}
	for section in myconfig :
	        for key in myconfig[section] :
                	configlist.update({key:myconfig[section][key]})

	if request.method == "POST" :
		myconfig = request.form.to_dict()
		Config.wrConfig(myconfig)

		Config.dirtyFlag = True
		return redirect(url_for('status') )
	return render_template("config.html", content = configlist, ds = Utils.datestring(), dirty = isdirty() )

@App.route('/')
def status() :
	#pdb.set_trace()
	varlist={"iGate Call":Config.ConfigDict["call"] , "Connect to APRS-IS":Config.ConfigDict["en_aprsis"] , 
		"APRS-IS Login":Config.Login," ":" ",
		"iGate LAT":Config.ConfigDict["lat"] , "iGate LON":Config.ConfigDict["lon"] , 
		"iGate Altitude":Config.ConfigDict["height"] , " " :" ",
		"Sensor BME280":Config.ConfigDict["en_bme280"], 
		"Temperatur":Config.Temperature, "Luftdruck":Config.AirPressureNN, "Luftfeuchtigkeit":Config.Humidity," ":" ",
		"Last Rx":Config.LastRx, "Last Message":Config.LastMsg,"RX Count": Config.RxCount,
		"RSSI": Config.RSSI, "Pkt RSSI": Config.PktRSSI, "SNR" : Config.SNR, "APRS-IS Message": Config.MsgSent,
		"Packet Err": Config.PktErr, 
		"Wx-Data": Config.ConfigDict["en_wxdata"] ,
		"Beacon Intervall": Config.ConfigDict["beaconinterval"] , "Beacon Message": Config.ConfigDict["beaconmsg"],
		"Uptime": Utils.elapsedTime(),"LoopCnt ":Config.loopmax,  
		"Version" : Config.Version 
	}

	return render_template("status.html", content = varlist, ds = Utils.datestring(), dirty = isdirty())

@App.route('/about/')
def about() :
	#pdb.set_trace()
	return render_template('about.html', ds = Utils.datestring(), dirty = isdirty())

@App.route('/wx/')
def wx() :
	#pdb.set_trace()
	wxlist = [Config.Temperature, Config.Humidity, Config.AirPressureNN]
	if (Config.ConfigDict["en_wxdata"]) :
		wx = "Show"
	else :	
		wx = "Hide"
	return render_template('wx.html', content = wxlist, WxData = wx, ds = Utils.datestring(), dirty = isdirty())
	#pdb.set_trace()


if __name__ == '__main__':
#	x = threading.Thread(target=run, args=(1,))
#	x.start()
#	while 1 :
#		time.sleep(10)
	Config.StartTime = time.time()
	Config.initConfigDict(Config.getConfig())
	run("0.0.0.0")
	pdb.set_trace()
