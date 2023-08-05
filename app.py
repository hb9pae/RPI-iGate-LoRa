
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


app = Flask(__name__)
app.logger.removeHandler(default_handler)
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
	 app.run(ip, debug=False)

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

@app.route("/log/",  methods=['GET', 'POST'] )
def log() :
	myLog =  "/var/log/iGate.log"
	#pdb.set_trace()
	cmd = ("tail", "-100", myLog)
	res = subprocess.run(cmd, capture_output=True, text=True)
	out = res.stdout.split("\n")
	#pdb.set_trace()
	return render_template("log.html", content = out, ds = datestring(), dirty=isdirty())


@app.route("/reboot")
def reboot() :
	Config.reboot = True
	Config.dirtyFlag = False
	return redirect(url_for('status') )


@app.route("/config/",  methods=['GET', 'POST'] )
def config() :
	myconfig = Config.getConfig(Config.myConfig)

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

@app.route('/')
def status() :
	#pdb.set_trace()
	varlist={"iGate Call":Config.CALL, "Connect to APRS-IS":Config.EN_APRSIS, " ":" ",
		"iGate LAT":Config.LAT, "iGate LON":Config.LON, "iGate Altitude":Config.HEIGHT, " " :" ",
		"Sensor BME280":Config.EN_BME280, "BME280 Intervall": Config.BMEINTERVAL, 
		"Temperatur":Config.Temperature, "Luftdruck":Config.AirPressureNN, "Luftfeuchtigkeit":Config.Humidity," ":" ",
		"Last Message":Config.LastMsg,"RSSI": Config.RSSI, "Pkt RSSI": Config.PktRSSI, "SNR" : Config.SNR, 
		"Packet Err": Config.PktErr, "APRS-IS Message": Config.MsgSent,"RX Count": Config.RxCount,
		"Wx-Data": Config.EN_WXDATA, "WX Intervall" : Config.WXINTERVAL,
		"Beacon Intervall": Config.BEACONINTERVAL, "Beacon Message": Config.BEACONMESSAGE, "Uptime": elapsedTime(), 
		"Version" : Config.Version, "DirtyFlag": Config.dirtyFlag
	}

	return render_template("status.html", content = varlist, ds = datestring(), dirty = isdirty())

@app.route('/about/')
def about() :
	#pdb.set_trace()
	return render_template('about.html', ds = datestring(), dirty = isdirty())

@app.route('/wx/')
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
#	x = threading.Thread(target=run, args=(1,))
#	x.start()
#	while 1 :
#		time.sleep(10)
	run("0.0.0.0")
