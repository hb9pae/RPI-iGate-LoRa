README.md, 2023-06-27, hb9pae

#	Copyright
(c) 2023, Peter Stirnimann, hb9pae@swiss-artg.ch

#	LoRa APRS-iGate für den Raspberry PI

##	Allgemeines
Der LoRa APRS-iGate empfängt LoRa APRS-Positionssignale und leitet diese an das 
APRS-Datenbank weiter. Diese Positionsmeldungen können anschliessend unter http://aprs.fi 
angezeigt werden. 

Das Python Programm IGate.py steuert das LoRa RPI-Board der SWISS-ARTG mit dem RF95W Chip RF-Hope
als LoRa-Empfänger. Weitere Informationen zum RPI-Board unter:  https://www.swiss-artg.ch/index.php?id=174

###	Modifikation RPI-Board
Das RPI-Board der SWISS-ARTG muss für den Interrupt-Betrieb modifiziert werden.
Verbinde Pin14 vom RFM96W (DIO-0) mit Pin 11 (BCM17) vom RPI 40-pol Header.

### 	Installation
Für die Installation wird ein IMAGE zur Verfügung gestellt. Kopiere das Image-File 
mit einem Imager-Programm (z.B. Raspberry Pi Imager) auf eine SD-Karte (mind. 8 GB).

## 	Inbetriebnahme
	- LoRa RPI-Board auf dem Raspberry PI aufstecken.
	- Die programmierte SD-Karte im RPI einstecken.
	- RPI mit dem lokalen Netzwerk verbinden.
	- PRI mit der Stromversorgung (5VDC) versorgen.

Nach dem ersten Start des Raspberry PI wird das Filesystem auf der SD-Karte expandiert, es 
folgen mehrere Restarts. Nach dem erfolgreichen Start des Programmes erscheint der Welcome-Bildschirm 
auf dem OLED-Display.

## 	Bedienung
Die drei unteren Tasten auf dem RPI-Board wählen den Anzeigemode

	-	Taste links >  Status 
	-	Taste mitte	>  Konfiguration
	-	Taste rechts > Letzte Meldung 	 

Die beiden oberen Tasten neben dem Display aktivieren den Welcome-Screen.
 
## 	Konfiguration 
Die Konfiguration der persönlichen Daten (Rufzeichen, Koordinaten etc.) erfolgt über einen Web-Browser.
Die IP-Adresse kann im Menue "Status" (untere Taste links) ausgelesen werden.

Web-Browser öffnen und im der Adresszeile die IP-Adresse eingeben zB. http://192.168.0.111.
Die Ausgabe erfolgt über den Apache Proxy-Server  
  
## 	Bibliotheken
Das Python Programm verwendet die Bibliothek loralib.so (https://github.com/wdomski/LoRa-RaspberryPi), 
Zudem sind folgende Python Pakete notwendig:

**Package            Version**
	Adafruit-GPIO    1.0.3
	Adafruit-PureIO  1.1.11
	Adafruit-SSD1306 1.6.2
	aprslib          0.7.2
	Pillow           9.5.0
	pip              23.1.2
	pkg_resources    0.0.0
	setuptools       40.8.0
	smbus2           0.4.2
	spidev           3.6


## 	Hardwarekonfiguration
Der LoRa Treiber erwartet folgende Hardwarekonfiguration
    (File LORA/lora.c)
    int ssPin = 10; //ChipSelect  BCM 8
    int dio0  = 21; //IRQ  BCM 5
    int RST   = 22; //RESET BCM 6

 
