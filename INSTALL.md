Installation iGate 
------------------

2023-06-15
2023-07-07, hb9pae

sudo apt update
sudo apt upgrade
sudo apt install git

echo "alias python=/usr/bin/python3" >> ~/.bashrc
source ~/.bashrc


sudo apt install python3-pip
sudo apt install python3-dev 
sudo apt install libopenjp2-7-dev
sudo apt install libtiff-dev

sudo  python -m pip install --upgrade pip setuptools wheel
sudo pip install Adafruit-SSD1306
sudo python -m pip install --upgrade pip
sudo python -m pip install --upgrade Pillow

sudo pip install smbus2
sudo pip install loralib
sudo pip install aprslib
sudo pip install flask

wget https://github.com/WiringPi/WiringPi/releases/download/2.61-1/wiringpi-2.61-1-armhf.deb
	sudo dpkg -i wiringpi-2.61-1-armhf.deb

raspi-config 
- ssh enable
- i2c enable 
- spi enable
- serial enable
	
sudo chmod 777 /var/log/

git clone https://github.com/hb9pae/RPI-iGate-LoRa.git

cd RPI-iGate-LoRa
cd LORA
	Kontrolliere/passe die  aktuelle Python Version im Makefile an:
	Python Version 3.9 

	make clean
	male all
	
Test Library:	
./lora_app.exe test

hb9pae@LORAGW:~/RPI-iGate-LoRa/LORA $ ./lora_app.exe test
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
-------------

cp loralib.so ../

-------------

