echo '<< SSD1309 Installation >>'
echo '<< Remember to enable SPI in sudo raspi-config >>'
echo '<< By VincentChan >>'

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo pip3 install --upgrade setuptools
sudo pip3 install RPI.GPIO
sudo usermod -a -G i2c,spi,gpio pi
sudo apt install python3-dev python3-pip libfreetype6-dev libjpeg-dev build-essential
sudo apt install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev

echo 'Please reboot your system ...'
echo 'Please execute phase 2 after reboot...'
