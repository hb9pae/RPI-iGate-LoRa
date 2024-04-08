
#!/bin/bash

# 2024-03-29, 2023-06-27, hb9pae

# Script zur Installation LoRa APRS Igate
# das Script generiert eine virtuelles Envviroment und kopiert dann die Programmdaten
#

#set -x

LoraRoot="/opt/"
LoraSrc="https://github.com/hb9pae/RPI-iGate-LoRa.git"
LoraHome="$LoraRoot/lorapy"
LoraUser="pi"

WiringPi="https://github.com/WiringPi/WiringPi/releases/download/3.2/wiringpi_3.2_arm64.deb"

enable_interfaces() {
# enable i2c and spi interfaces
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_serial 2
}

update() {
	sudo apt update
	sudo apt upgrade  -y
	echo "Upgrade done" 
}

function install_progs {
	# install packages
	for PROGS in "git" "python3-pip" "python3-dev" "libopenjp2-7-dev" "libtiff-dev" "ibrrd-dev" "libpython3-dev"
		do
			sudo apt install  "$PROGS" -y
			echo "$PROGS installed"
		done
}

function install_wiringpi() {
	wget $WiringPi
	sudo dpkg -i wiringpi_*
}

function make_virtenv {
	cd $LoraRoot
	/usr/bin/python3 -m venv lora
	cd $LoraRoot/lora/
	source bin/activate
}

function install_PyLibs {
	python3 -m pip install --upgrade pip

	pip3 install smbus2
	pip3 install loralib
	pip3 install aprslib
	pip3 install flask
	pip3 install Adafruit-SSD1306
	pip3 install rrdtool
	pip3 install RPi.GPIO
	python3 -m pip install --upgrade Pillow

}

function make_userauth {
	sudo chmod 777 $LoraRoot
	sudo usermod -aG adm $LoraUser
	sudo chmod 777 /var/log
}

#------- Script ----------
echo "Start Installer"
if [ -d "$LoraHome" ]; then
	rm -r  $LoraHome
	echo "$LoraHome deleted..."
fi

cd $LoraRoot 
update
install_progs
install_wiringpi
echo "enable_interfaces"
enable_interfaces
echo "make User Auth"
make_userauth
echo "make virt env"
make_virtenv 
echo "install Pylibs"
install_PyLibs

cd $LoraRoot 
git clone $LoraSrc

if [ $? -ne 0 ]; then
    echo "Error occurred."
fi





