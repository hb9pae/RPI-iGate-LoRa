Installation iGate 
------------------

2023-06-15


sudo apt update
sudo apt upgrade 
sudo apt install git

echo "alias python=/usr/bin/python3" >> ~/.bashrc
source ~/.bashrc

https://github.com/hb9pae/RPI-iGate-LoRa.git

git clone https://github.com/hb9pae/RPI-iGate-LoRa.git
sudo apt-get install python3-dev 

Raspi-Config:	
	SSH enable
	SPI enable
	i2C enable
	serial enable

	
cd RPI-iGate-LoRa
cd LORA
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

sudo apt install python3-pip
sudo apt-get install libopenjp2-7-dev 
sudo apt-get install libtiff-dev


pip3 install Adafruit-SSD1306
pip3 install aprslib
pip3 install smbus2


python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow




git clone https://github.com/hb9pae/RPI-iGate-LoRa.git


