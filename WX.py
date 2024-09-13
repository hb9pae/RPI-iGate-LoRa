#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul  WX
"""

__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__ = "hb9pae@gmail.com"

import os, sys
import pdb
import logging
import Config
import BME280
import APRS
import rrdtool
import datetime


def writeRRD(file, temperature, pressure, humidity) :
	rrdtool.update(file, 'N:%f:%f:%f' % (temperature, humidity, pressure))
	logging.info('Update RRD: N:%f:%f:%f' % (temperature, humidity, pressure))

def createRRD(file) :
	rrdtool.create(file, "--step", "300", "--start", 'N',
		"DS:temp1:GAUGE:1200:-40:50",
		"DS:humid:GAUGE:1200:0:100",
		"DS:baro:GAUGE:1200:850:1250",
		"RRA:AVERAGE:0.5:1:2880",
		"RRA:AVERAGE:0.5:6:700",
		"RRA:AVERAGE:0.5:24:775",
		"RRA:AVERAGE:0.5:144:1500",
		"RRA:AVERAGE:0.5:288:2000",
		"RRA:MIN:0.5:1:600",
		"RRA:MIN:0.5:6:700",
		"RRA:MIN:0.5:24:775",
		"RRA:MIN:0.5:144:1500",
		"RRA:MIN:0.5:288:2000",
		"RRA:MAX:0.5:6:700",
		"RRA:MAX:0.5:24:775",
		"RRA:MAX:0.5:144:1500",
		"RRA:MAX:0.5:288:2000"
	)

def BMEInterval() :
	readBME280()
	wxGraph(Config.WXrrd)

def readBME280() :
	if not (Config.EN_BME280) :
		return				# no BME280 available
	if not (os.path.exists(Config.WXrrd)) :
		createRRD(Config.WXrrd)
		logging.info("Created new RRD-DB: %s" % (Config.WXrrd))

	logging.info("Read BME280")
	try :
		_altitude = int(Config.HEIGHT)
	except:
		logging.info("Wrong Altitude format, assume 400m asl")
		_altitude = 400

	try :
		#pdb.set_trace()
		(temp, press_nn, hum) = BME280.getBME280(_altitude)
		writeRRD(Config.WXrrd, temp, press_nn, hum)
	except :
		Config.EN_BME280 = False
		Config.EN_WXDATA = False
		logging.info("BME280 not available, BME280 and WX-DATA disabled")

	Config.Temperature = round(temp,2)
	Config.AirPressureNN = round(press_nn,1)
	Config.Humidity = round(hum,1)

def WxReport() :
	#pdb.set_trace()
	if (Config.EN_WXDATA) :
		logging.info("Prepare WxReport")
		dt = datetime.datetime.now(datetime.timezone.utc)
		_DHM = dt.strftime("@%d%H%Mz")
		_pos = Config.POS[0] + "/" + Config.POS[1] 
		_wind  = "_.../...g..."
		_tempf = (Config.Temperature * 1.8) + 32 # APRS benötigt Farenheit 
		_temp = "t" + str(int(round(_tempf,1)))
		_rain = "r...p...P..."
		_hum = "h" + str(int(round(Config.Humidity)))
		_press = "b" + str(int(10*round(Config.AirPressureNN,1)))
		_id = " BME280"
		_WxReport = Config.CALL + ">APRS:" +_DHM + _pos + _wind + _temp + _rain + _hum + _press  + _id
		APRS.sendMsg(_WxReport)

def wxGraph(rrd) :
	rrdtool.graph( 
	"static/wx-temp-d.png", 
	"--start", "-1d", 
	"--vertical-label", "Grad Celsius",
	"--watermark=hb9pae@swiss-artg.ch",
	"-w 800",
	"--title=Aussentemperatur",
	"DEF:t1=%s:temp1:AVERAGE" %(rrd),
	"LINE1:t1#0000FF:Temperatur",
	"GPRINT:t1:LAST:Aktuell %5.2lf °C",
	"GPRINT:t1:AVERAGE:Mittlelwert  %5.2lf °C",
	"GPRINT:t1:MAX: Maximal %5.2lf °C"
	)

	rrdtool.graph(
	"static/wx-humid-d.png", 
	"--start", "-1d", 
	"--vertical-label", "Rel. Feuchtigkeit",
	"--watermark=hb9pae@swiss-artg.ch",
	"-w 800",
	"--title=Rel. Feuchtigkeit",
	"--upper-limit=100", "--lower-limit=0",
	"DEF:h1=%s:humid:AVERAGE" % (rrd),
	"LINE1:h1#0000FF:Rel. Feuchtigkeit",
	"GPRINT:h1:LAST:Aktuell %5.0lf %%",
	"GPRINT:h1:AVERAGE:Mittlelwert  %5.0lf %%",
	"GPRINT:h1:MAX: Maximal %5.0lf %%"
	)

	rrdtool.graph( "static/wx-barom-d.png", 
	"--start", "-1d", 
	"--vertical-label", "Rel. Luftdruck",
	"--watermark=hb9pae@swiss-artg.ch",
	"-w 800",
	"--title=Rel. Luftdruck",
	"DEF:p1=%s:baro:AVERAGE" % (rrd),
	"LINE1:p1#0000FF:Rel. Luftdruck",
	"GPRINT:p1:LAST:Aktuell %5.0lf hpa",
	"GPRINT:p1:AVERAGE:Mittlelwert  %5.0lf hpa",
	"GPRINT:p1:MAX: Maximal %5.0lf hpa"
	)

