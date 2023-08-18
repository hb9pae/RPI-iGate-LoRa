#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul HMI.py
Anzeige auf dem OLED-Modul
# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
"""

# hb9pae, 2023-04-19

import Adafruit_SSD1306
import RPi.GPIO as GPIO

import time
import socket
import logging

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import pdb

#Importiere Globale Variablen
import Config

# Zuordnung Tasten zum GPIO
#SW1 = 21	# Welcome Menu
#SW2 = 20	# Status Display
#SW3 = 16	# Config Display
#SW4 = 19	# Packet Display
#SW5 = 26	# Welcom Menu


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

def call_sw(channel):
	menudict = {21:0, 20:0, 16:1, 19:2, 26:3}  # Translate BCM-Pin:Display.Menu 
	Config.Menu = menudict.get(channel)

def initbutton() :
	#GPIO.cleanup(GPIO.BCM)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup([21, 20, 16, 19, 26], GPIO.IN)

	GPIO.add_event_detect(21, GPIO.RISING, callback=call_sw, bouncetime=200)  # add rising e$
	GPIO.add_event_detect(20, GPIO.RISING, callback=call_sw, bouncetime=200)  # add rising e$
	GPIO.add_event_detect(16, GPIO.RISING, callback=call_sw, bouncetime=200)  # add rising e$
	GPIO.add_event_detect(19, GPIO.RISING, callback=call_sw, bouncetime=200)  # add rising e$
	GPIO.add_event_detect(26, GPIO.RISING, callback=call_sw, bouncetime=200)  # add rising e$
	Config.Menu = 0
	Config.MenuOld = 9

def initdisplay() :
	RST = None
	# 128x64 display with hardware I2C:
	disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

	# Initialize library.
	disp.begin()

	# Clear display.
	disp.clear()
	disp.display()
	return(disp)

def display(page) :
	display =initdisplay()
	width = display.width
	height = display.height
	image = Image.new('1', (width, height))

	# First define some constants to allow easy update
	padding = 2
	menu_width = 40
	menu_height = 12
	top = padding
	bottom = height-padding

	# define start menu
	x = padding
	x1 = x+menu_width
	y = height-menu_height
	y1 = height - padding
	#print("Menu positions X: %d Y: %d X1: %d y1:%d" % (x,y,x1,y1))

	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)

	# Draw a black filled box to clear the image.
	draw.rectangle((0,0,width-padding,height-padding), outline=0, fill=0)

	# Load default font.
	font = ImageFont.load_default()
	font0 = ImageFont.load_default()
	font1 = ImageFont.truetype("Vera.ttf",10)
	font2 = ImageFont.truetype("Vera.ttf",16)
	#draw rectangle for active menu

	if (page == 0) :		# WELCOME
		#print("", top, top, height-padding, width-padding)
		draw.rectangle((2, 2, 125, 60 ), outline=255, fill=255)
		draw.text((25, 1),	"Welcome!",  font=font2, fill=0)
		draw.text((4, 21),	"LoRA iGate",  font=font1, fill=0)
		draw.text((4, 35),	 Config.CALL,  font=font1, fill=0)
		draw.text((4, 49),	"V " + Config.Version  + " (c)HB9PAE",  font=font1, fill=0)

	elif (page == 1) :		# STATUS
		draw.rectangle((x, y, x1, y1), outline=255, fill=255)
		draw.text((8, 50),	'Stat.',  font=font1, fill=0)
		draw.text((53, 50),	'Conf.',  font=font1, fill=255)
		draw.text((100, 50),	'Pack.',  font=font1, fill=255)


		wxT = "{:5.1f}°".format(Config.Temperature)
		wxH = "{:7.1f}%".format(Config.Humidity)
		wxP = "{:8.1f}hPa".format(Config.AirPressureNN)

		draw.text((4, 4),	"IP:" + Config.IP, font=font1, fill=255)
		draw.text((4, 13),	"Call:" + Config.CALL , font=font1, fill=255)
		draw.text((4, 22),	"APRS Status: " + Config.AprsStat, font=font1, fill=255)
		draw.text((4, 31),	"WX:  Temp:   Hum:   Pres."  , font=font1, fill=255)
		draw.text((4, 40),	str(wxT) + str(wxH) + str(wxP), font=font1, fill=255)

	elif (page == 2) :		# CONFIG
		draw.rectangle((x+45, y, x1+45, y1), outline=255, fill=255)
		draw.text((8, 50),    'Stat.',  font=font1, fill=255)
		draw.text((53, 50),   'Conf.',  font=font1, fill=0)
		draw.text((100, 50),   'Pack.',  font=font1, fill=255)

		draw.text((4, 4),	"Call:   " + Config.CALL, font=font1, fill=255)
		draw.text((4, 13),	"Position: " + str(Config.LAT) + "/" + str(Config.LON),  font=font1, fill=255)
		draw.text((4, 22),	"Altitude: " + str(Config.HEIGHT),  font=font1, fill=255)
		draw.text((4, 31),	"EN-BME280:   " + str(Config.EN_BME280),  font=font1, fill=255)

	elif (page == 3) :		# PACKET
		draw.rectangle((x+90, y, x1+90, y1), outline=255, fill=255)
		draw.text((8, 50),    'Stat.',  font=font1, fill=255)
		draw.text((53, 50),   'Conf.',  font=font1, fill=255)
		draw.text((100, 50),   'Pack.',  font=font1, fill=0)

		draw.text((4, 4),	"Last Message:",  font=font1, fill=255)
		draw.text((4, 13),	Config.LastPkt, font=font1, fill=255)
		draw.text((4, 22),	"IP:" + Config.IP, font=font1, fill=255)
		draw.text((4, 31),	"APRS Status:  " + Config.AprsStat, font=font1, fill=255)

	elif (page == 4) :		# No IP, check Internet
		#print("", top, top, height-padding, width-padding)
		draw.rectangle((2, 2, 125, 60 ), outline=255, fill=255)
		draw.text((25, 1),	"Error!",  font=font2, fill=0)
		draw.text((4, 25),	"Check Internet Connection",  font=font1, fill=0)
		draw.text((4, 49),	"V " + Config.Version  + " (c)HB9PAE",  font=font1, fill=0)


	display.image(image)
	display.display()
	Config.DisplayOn = time.time()	


def main() :
	global MENU
	MYIP = getip()
	initbutton()
	display(1)
	time.sleep(2)

	while True :

		if (MENU == 1) :
			display(1)
			MENU = 0
		elif (MENU == 2) :
			display(2)
			MENU = 0
		elif (MENU == 3) :
			display(3)
			MENU = 0
		elif (MENU == 4) :
			display(4)
			MENU = 0
		elif (MENU == 5) :
			display(0)
			MENU = 0
		else :
			time.sleep(0.1)



if __name__ == "__main__":
	main()
