#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul Button.py
Abfragen der Push-Buttons und initialisierung der Anzeige
# Idee https://stackoverflow.com/questions/75178435/python-event-handler-for-background-task-complete
"""


from threading import Thread
import time
import pdb
import Config
from gpiozero import Button
from signal import pause

#Zuordung Btn:Menu = {21:0, 20:0, 16:1, 19:2, 26:3}  # Translate BCM-Pin:Display.Menu 

def BTN16():
	#global menu
	Config.Menu = 1

def BTN19():
	#global menu
	Config.Menu = 2

def BTN20():
	#global menu
	#pdb.set_trace()
	Config.Menu = 0

def BTN21():
	#global menu
	Config.Menu = 0

def BTN26():
	#global menu
	Config.Menu = 3


def read_buttons():
	btn16 = Button(16, pull_up=False)
	btn19 = Button(19, pull_up=False)
	btn20 = Button(20, pull_up=False)
	btn21 = Button(21, pull_up=False)
	btn26 = Button(26, pull_up=False)

	btn16.when_released = BTN16
	btn19.when_released = BTN19
	btn20.when_released = BTN20
	btn21.when_released = BTN21
	btn26.when_released = BTN26

	while True:
		time.sleep(0.5)
		pause()

def init_btnthread() :
	#global menu
	Config.Menu = 0
	button_thread = Thread(target=read_buttons, daemon=True)
	button_thread.start()


def main():
	global menu

	Config.Menu = 0
	button_thread = Thread(target=read_buttons, daemon=True)
	button_thread.start()

	i=0
	print("start main")
	while True:
		#pdb.set_trace()
		if (menu > 0) :
			print("Menu: ", menu)
			menu = 0
		time.sleep(0.1)

if __name__ == "__main__":
	main()
