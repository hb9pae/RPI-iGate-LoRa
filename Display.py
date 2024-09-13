#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul display.py
Anzeige auf dem OLED-Modul
Examples for a 128x64 px SSD1306 oled display.
https://pypi.org/project/oled-text/
"""

# hb9pae, 2024-08-23

__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__ = "hb9pae@gmail.com"

import time
import logging
import pdb

import busio
from board import SCL, SDA

#Importiere Globale Variablen
import Config

from oled_text import OledText, Layout64, BigLine, SmallLine
i2c = busio.I2C(SCL, SDA)
oled = OledText(i2c, 128, 64)


def init() :
	oled.layout = Layout64.layout_icon_only()
	# A single FontAwesome icon (https://fontawesome.com/cheatsheet/free/solid)
	oled.text('\uf58b', 1)
	time.sleep(0.5)

def display(page) :
	if (page == 0) :		# WELCOME
		oled.layout = Layout64.layout_5small()
		oled.auto_show = False
		oled.text("WELCOME LoRa-iGate", 1)
		#oled.text(" LoRa iGate", 2)
		oled.text(" " + Config.CALL, 2)
		oled.text("  ",3)
		oled.text(" V " + Config.Version + "(c) HB9PAE", 4)
		oled.text("Stat   Pack   Conf",5)

	elif (page == 1) :		# STATUS
		oled.layout = Layout64.layout_5small()
		oled.auto_show = False
		oled.text("STATUS " + Config.CALL, 1)
		oled.text(" " + Config.IP, 2)
		oled.text(" APRS-IS: " + Config.AprsStat, 3)
		oled.text(" Uptime: " + Config.upTime() ,4)
		oled.text("Stat   Pack   Conf",5)

	elif (page == 2) :
		oled.layout = Layout64.layout_5small()
		oled.auto_show = False
		oled.text("LoRa-RX: " + Config.LastRx[-9:], 1)
		#pdb.set_trace()
		oled.text(" From: " + Config.From.ljust(10), 2)
		oled.text(" To:   " + Config.To.ljust(10), 3)
		oled.text(" Cnt:  " + str(Config.PktSize), 4)
		oled.text("Stat   Pack   Conf",5)

	elif (page == 3) :
		oled.layout = Layout64.layout_5small()
		oled.auto_show = False
		oled.text("CONFIG", 1)
		oled.text(" Call: " + Config.CALL, 2)
		oled.text(" Pos: " + str(Config.LAT[:5]) + "/" + str(Config.LON[:5]), 3)
		oled.text(" Alt: " + str(Config.HEIGHT) + "m asl", 4)
		oled.text("Stat   Pack   Conf",5)

	elif (page == 4) :
		oled.layout = Layout64.layout_5small()
		oled.auto_show = False

		if Config.EN_BME280 :
			wxT = "{:8.1f} °".format(Config.Temperature).rjust(10)
			wxH = "{:8.1f} %".format(Config.Humidity).rjust(10)
			wxP = "{:8.1f}hPa".format(Config.AirPressureNN).rjust(10)

			oled.text("WETTER", 1)
			oled.text(" Temp: " + str(wxT), 2)
			oled.text(" Hum:  " + str(wxH), 3)
			oled.text(" Press:" + str(wxP), 4)
			oled.text("Stat   Pack   Conf",5)
		else :
			oled.text("WETTER", 1)
			oled.text(" ", 2)
			oled.text("not Available".center(19), 3)
			oled.text(" ", 4)
			oled.text("Stat   Pack   Conf",5)


	oled.show()
	oled.auto_show = True
	Config.DisplayOn = time.time()
	Config.Menu = 99
	Config.MenuLast =  page

def clear() :
	oled = OledText(i2c, 128, 64)

def main() :
	Config.IP = "111.222.333.444"
	Config.AprsStat = "Connected"
	Config.LAT = "45.5555555"
	Config.LON = "8.55555555"
	Config.HEIGHT = "455"
	Config.CALL = "HB9PAE-12"
	init()
	Config.EN_BME280 = True

	i = 0
	while 1 :
		display(i)
		i += 1
		if i >  4 :
			i = 0 
		time.sleep(5)
		print("Clear")
		clear()
		time.sleep(5)

	pdb.set_trace()


if __name__ == "__main__":
	main()
