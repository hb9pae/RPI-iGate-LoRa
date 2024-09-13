#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul button.py
Auswertung der Tasten, Menusteuerung
# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
"""


__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2024"
__email__ = "hb9pae@gmail.com"

# hb9pae, 2023-04-19, 2024-08-24

from gpiozero import Button

import socket
import time
import logging
import pdb

#Importiere Globale Variablen
import Config

# Define the Reset Pin

# Zuordnung Tasten zum GPIO
#SW1 = 21	# Welcome Menu
#SW2 = 20	# Status Display
#SW3 = 16	# Config Display
#SW4 = 19	# Packet Display
#SW5 = 26	# Welcom Menu

BTN_DEBUG=False

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

def call_menu16(button) :
	if BTN_DEBUG :
		print("BTN 16")

	Config.Menu = 1

def call_menu19(button) :
	if BTN_DEBUG :
		print("BTN 19")

	Config.Menu = 2

def call_menu20(button) :
	if BTN_DEBUG :
		print("BTN 20")

	# Info screen
	x = Config.MenuLast -1 
	if ( 0 <= x <= 4 ) :
		Config.Menu = x
	else :
		Config.Menu = 4

def call_menu21(button) :
	if BTN_DEBUG :
		print("BTN 21")

	# Info screen
	x = Config.MenuLast +1 
	if ( 0 <= x <= 4 ) :
		Config.Menu = x
	else :
		Config.Menu = 0

def call_menu26(button) :
	if BTN_DEBUG :
		print("BTN 26")

	Config.Menu = 3

def init() :
	btn16 = Button(16,  pull_up=False, bounce_time=0.05)
	btn16.when_pressed = call_menu16
	btn19 = Button(19,  pull_up=False, bounce_time=0.05)
	btn19.when_pressed = call_menu19
	btn20 = Button(20,  pull_up=False, bounce_time=0.05)
	btn20.when_pressed = call_menu20
	btn21 = Button(21,  pull_up=False, bounce_time=0.05)
	btn21.when_pressed = call_menu21
	btn26 = Button(26,  pull_up=False, bounce_time=0.05)
	btn26.when_pressed = call_menu26

	Config.Menu = 0
	Config.MenuOld = 0

def main() :
	print("IP:" , getip())
	init()
#	pdb.set_trace()
#	wait = input("Press Enter to continue.")

	while (1) :
		print("Menu: ", Config.Menu)
		time.sleep(5)


if __name__ == "__main__":
	main()
