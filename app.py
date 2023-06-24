
from  flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import datetime, time
import pdb
import configparser, json
import Config
import threading
import subprocess 
import time

from flask.logging import default_handler
import logging


#parameterfile= "./igate.ini"
# https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application
# https://stackoverflow.com/questions/29547200/how-to-get-a-python-dict-into-an-html-template-using-flask-jinja2

app = Flask(__name__)
app.logger.removeHandler(default_handler)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def  run(ip) :
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
	now = datetime.datetime.now() 
	header1 = "# APRS iGate configuration\n# (c) hb9pae@gmail.com"
	header2 = now.strftime("# Created (app): %d/%m/%Y %H:%M:%S\n")
	f = open(Config.myConfig, "w")
	f.writelines(header1)
	f.writelines(header2)
	f.close()
	#pdb.set_trace()
	config = configparser.ConfigParser()
	config["APRS"] = newconf
	with open(Config.myConfig, "a") as configfile :
		config.write(configfile)

@app.route("/log/",  methods=['GET', 'POST'] )
def log() :
	cmd = ("tail", "-100", "/var/log/iGate.log")
	res = subprocess.run(cmd, capture_output=True, text=True)
	out = res.stdout.split("\n")
	#pdb.set_trace()
	return render_template("log.html", content = out )


@app.route("/config/",  methods=['GET', 'POST'] )
def config() :
	myconfig = Config.getConfig(Config.myConfig)

	configlist={}
	for section in myconfig :
	        for key in myconfig[section] :
                	configlist.update({key:myconfig[section][key]})

	if request.method == "POST" :
		myconfig = request.form.to_dict()
		saveconfig(myconfig)

		myconf = Config.getConfig(Config.myConfig)
		Config.setGlobals(myconf)

		Config.dirtyFlag = True
		return redirect(url_for('status') )

	#pdb.set_trace()
	return render_template("config.html", content = configlist )

@app.route('/')
def status() :
	#pdb.set_trace()
	if (Config.BME280.lower() in ['true', '1', 'yes'] ) :
		varlist={"iGate Call":Config.CALL, "Connect to APRS-IS":Config.APRSIS, " ":" ",
			"iGate LAT":Config.LAT, "iGate LON":Config.LON, "iGate Altitude":Config.HEIGHT, " " :" ",
			"Temperature":Config.Temperature, "AirPressure NN":Config.AirPressureNN, "Humidity":Config.Humidity," ":" ",
			"Last Mssage":Config.LastMsg,"Current  RRSI": Config.CurrtRRSI, "Last Pkt RSSI": Config.LastPktRRSI,
			"Packet Err": Config.PktErr, "Packet Sent": Config.PktSent,"RX Count": Config.RxCount, "SNR": Config.SNR,
			"Uptime": elapsedTime()
		}
	else : 
		varlist={"iGate Call":Config.CALL, "Connect to APRS-IS":Config.APRSIS, " ":" ",
			"iGate LAT":Config.LAT, "iGate LON":Config.LON, "iGate Altitude":Config.HEIGHT, " " :" ",
			"Last Mssage":Config.LastMsg,"Current  RRSI": Config.CurrtRRSI, "Last Pkt RSSI": Config.LastPktRRSI,
			"Packet Err": Config.PktErr, "Packet Sent": Config.PktSent,"RX Count": Config.RxCount, "SNR": Config.SNR,
			"Uptime": elapsedTime()
		}

	return render_template("index.html", content = varlist )


@app.route('/about/')
def about() :
	#pdb.set_trace()
	return render_template('about.html')


if __name__ == '__main__':
#	x = threading.Thread(target=run, args=(1,))
#	x.start()
#	while 1 :
#		time.sleep(10)
	run("1")
