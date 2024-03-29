#  Installation iGate 

Autor: hb9pae@gamail.com <br>
Revision: 2023-09-09, Version 1.0.1 <br>
Revision: 2023-09-10, Version 1.0.1a    Typo <br>
Revision: 2023-09-13, Version 1.0.1b    Typo <br>
Revision: 2024-03-24  Version 1.2		Boardrevision <br>

## Voraussetzungen
Diese Installationsanleitung basiert auf: 
-   Raspberry PI Modell 3 oder 4
-   Raspbian GNU/Linux 11 (bullseye)  (32 Bit / Raspian OS lite)
-   Python Version 3.9
-   LoRa iGate Aufsteckboard swiss-artg.ch (modifiziert oder Version 2)
-   Erstelle eine SD-Karte (> 8 GB) mit einem Benutzer "pi", erlaube den Zugriff über SSH 

###	Modifikation RPI-Board
Die neue Version vom RPI-Board muss nicht mehr modifiziert werden. Versions-Beschriftung 
oberhalb Diode D1: «231125».  

Das alte RPI-Board (Ohen Versionsbeschriftung) der SWISS-ARTG muss für den Interrupt-Betrieb 
modifiziert werden: 
Verbinde Pin14 vom RFM96W (DIO 0) mit Pin 11 (BCM17) vom RPI 40-pol Header.
<center> <img src="static/Board_mod1.jpeg" alt="Board Mod 1" style="height: 300px; width:300px;"/>
<img src="static/Board_mod2.jpeg" alt="Board Mod 2" style="height: 300px; width:300px;"/>
</center>

##  Installation 
Installiere unter dem Benutzer "root" folgende Pakete:
-   sudo apt update
-   sudo apt upgrade
-   sudo apt install git
-   sudo apt install python3-pip
-   sudo apt install python3-dev 
-   sudo apt install libopenjp2-7-dev
-   sudo apt install libtiff-dev
-   sudo apt-get install librrd-dev libpython3-dev

### Python3 Pakete, werden als Benutzer pi installiert: 
-   pip3 install smbus2
-   pip3 install loralib
-   pip3 install aprslib
-   pip3 install flask
-	pip3 install Pillow
-	pip3 install Adafruit-SSD1306
-	pip3 install rrdtool 

###  Installation der Python-Programme und setzen der Berechtigungen
Die Python Sourcen werden im Verzeichnis "/opt" installiert. 
-   sudo chmod 777 /opt/            # Erlaube Lese- und Schreib-Zugriff für alle User  
-   sudo usermod -aG adm pi		# Erlaube Lese- und Schreib-Zugriff im Verzeichnis </var/log> 
-   sudo chmod 777 /var/log		# Erlaube Lese und Schreibberechtigung Verzeichnis </var/log>

Wir installieren nun Wiring PI
-   cd /opt
-   wget https://github.com/WiringPi/WiringPi/releases/download/2.61-1/wiringpi-2.61-1-armhf.deb
-   sudo dpkg -i wiringpi-2.61-1-armhf.deb

Wir installieren nun die Python Programme:
-   cd /opt
-   git clone https://github.com/swiss-artg/LoRa-APRS_RPI-iGate 

### Konfiguration Raspberry PI Interface
Folgende  RPI Interface
-   sudo raspi-config 
	-	ssh enable
    -	i2c enable 
    -	spi enable
    -	serial interface enable
-	sudo reboot  

### Kompilieren und Test der Library
cd /opt/RPI-iGate-LoRa
cd LORA
	Passe die  aktuelle Python Version im Makefile an:
	Python Version 3.9 

-	make clean
-	make all

Wir testen die Bibliothek	
./lora_app.exe test

#### Ausgabe: 
```
$ ./lora_app.exe test

SX1276 detected, starting.
Print Register 
Version: 0x12
FRF_MSB: 0x6c
FRF_MID: 0x71
FRF_LSB: 0x99
Sync Word: 0x12
FIFO: 0x9a
OPMODE: 0x8d
FIFO Addr: 0x1
FIFO TX Base: 0x80
FIFO RX Base: 0x0
RX NB Bytes: 0x0
FIFO RX Current: 0x0
IRQ: 0x0
DIO 1: 0x0
DIO 2: 0x0
Modem Config: 0x72
Modem Config 2: 0xc4
Modem Config 3: 0xc
SYMB Timeout: 0x5
SNR: 0x0
PayLoad: 0x40
IRW: 0x0
PayLoad LNG: 0x80
Hop Period: 0xff
Sync Word: 0x12
Version: 0x12
```

Wir kopieren die Library in das Programmverzeichnis:
-	cp loralib.so ../

###	Logfile
Das LogFile befindet sich unter /var/log/iGate.log und wird vom Benutzer pi beschrieben.
Wir erstellen ein leeres Logfile und passen die Rechte an.
-	sudo touch /var/log/iGate.log
-	sudo chown pi:pi /var/log/iGate.log

### Systemdienste
Installiere folgende Systemdienste:

###	Startscript: 
-	sudo cp utils/igate.service  /etc/systemd/system
-	sudo systemctl enable igate.service
-	sudo systemctl start igate.service

###	LogRotate
-	sudo cp utils/igate  /etc/logrotate.d/