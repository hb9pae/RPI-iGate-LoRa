# Changelog  

** unreleased **

Branch DEB12 
2024-09-10 15:40 Commit V 0.1 alpha
 


- Umstellung auf Debian 12
   - Ergänzung lora.c, Markfile
   - 

- Virt. Envirement eingeführt

- File HMI.py aufgeteilt > button.py und display.py

	Lib RPI.GPIO unterstützt GPIO.add_event_detect(21, .... nicht mehr.
	Wechsel zur Python-Lib gpiozero mit neuer Syntax 

	Adafruit_SSD1305 ist outdatet, ersetzt du Circuit-Python Lib 
	adafruit_ssd1306, neue Syntax

LoraRX: testhalber werden die empfangenen Daten  mit aprsliv validiert. Falls Fehler
werden die Pakete abgespeichert. 
PArameter in igate.ini 



ToDo:
WX.py
	Skalierung Luftdruck-Diagramm verbessern, y-Skala von 960 - 1050 mBar mit Beschriftung.


  

