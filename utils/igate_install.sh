#!/bin/bash

# 2023-06-27, hb9pae

# Script zur Installation LoRa APRS Igate
# das Script generiert eine virtuelles Envviroment und kopiert dann die Programmdaten
#

#set -x

LoraRoot="./"
LoraSrc="https://github.com/hb9pae/RPI-iGate-LoRa.git"
LoraHome="$LoraRoot/lorapy"


enable_interfaces() {
# enable i2c and spi interfaces
raspi-config nonint do_i2c 0
raspi-config nonint do_spi 0
raspi-config nonint do_serial 2
}

update() {
	apt update
	apt upgrade  -y
	echo "Upgrade done" 
}

python3-dev
udo apt install python3-pip
sudo apt-get install libopenjp2-7-dev
sudo apt-get install libtiff-dev


function install_progs {
	# install packages
	for PROGS in "git" "screen" "libi2c-dev" "python3-dev" "python3-pip" "libopenjp2-7-dev" "libtiff-dev"
		do
			sudo apt install  "$PROGS" -y
			echo "$PROGS installed"
		done
}

install_wiringpi() {
	wget https://github.com/WiringPi/WiringPi/releases/download/2.61-1/wiringpi-2.61-1-armhf.deb
	sudo dpkg -i wiringpi-2.61-1-armhf.deb
}

function make_virtenv {
	mkdir $LoraHome
	cd $LoraHome
	/usr/bin/python3 -m venv env
	source $LoraHome/env/bin/activate
}


echo "Start Installer"
if [ -d "$LoraHome" ]; then
	rm -r  $LoraHome
	echo "$LoraHome deleted..."
fi

make_virtenv
install_progs


pip3 install Adafruit-SSD1306
pip3 install aprslib
pip3 install smbus2

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow


if [ $? -ne 0 ]; then
    echo "Error occurred."
fi


pip3 install Adafruit-SSD1306
pip3 install aprslib
pip3 install smbus2

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow

git clone $LoraSrc




