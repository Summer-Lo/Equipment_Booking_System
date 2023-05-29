echo '<< SSD1309 Installation >>'
echo '<< Remember to enable SPI in sudo raspi-config >>'
echo '<< By VincentChan >>'

cd /home/pi/Desktop/PolyU_Attendance_System/
git clone https://github.com/rm-hull/luma.examples.git
cd luma.examples
sudo -H pip3 install -e .

echo 'Installation Completed!'
