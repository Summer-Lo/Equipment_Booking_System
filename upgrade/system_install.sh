## Basic PAD system installation
## Author: Vincent Chan
## Date: 1 Sep 2021

## System update and upgrade
echo "Start system update & upgrade"
sudo apt-get update && sudo apt-get upgrade
sudo apt install figlet toilet
figlet -c PolyU PAD Install

echo "Install basic editor tools"
sudo apt-get install gedit
sudo apt-get install tmux

echo "Install OLED driver"
sudo usermod -a -G i2c,spi,gpio pi
sudo apt install python3-dev python3-pip libfreetype6-dev libjpeg-dev build-essential
sudo apt install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev
git clone https://github.com/rm-hull/luma.examples.git
cd luma.example
sudo -H pip3 install -e .

echo "Install keypad package"
pip3 install pad4pi

echo "Install hardware driver controller"
pip3 install evdev

echo "Install SFTP package"
pip3 install pysftp

echo "Install Bluetooth support"
sudo apt-get install bluetooth bluez blueman
pip3 install pybluez

echo "X728 UPS software install"
sudo apt-get -y install python3-smbus i2c-tools
git clone https://github.com/geekworm-com/x728
cd x728
sudo chmod +x *.sh
sudo ./x728-v1.0.sh

echo "MQTT Client install"
pip3 install pybluez

echo "System Update OK!"
echo "Editor OK!"
echo "OLED OK!"
echo "Keypad OK!"
echo "Hardware driver OK!"
echo "SFTP OK!"
echo "Bluetooth OK!"
echo "X728 OK!"

