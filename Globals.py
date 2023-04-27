#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul config.py
Enthält alle Globalen Variablen
"""

# hb9pae, 2023-04-24

import datetime


__version__     = "0.0.2"
__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2023"
__email__       = "hb9pae@gmail.com"


Version = __version__
myConfig = "./igate.ini"

RxCount = 0
Frequ   = 433775000
SR      = 12

StartTime = datetime.datetime.now()
DisplayTimeout = 60

Temperature = 1.0
AirPressureNN = 1.0
Humidity = 1.0

LastPkt = "--- None ---"
