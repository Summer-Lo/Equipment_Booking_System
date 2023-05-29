from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1309
from time import sleep
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#List out SPI channels
#ls -l /dev/spi*
#spidev<port>.<device>

font_file = '/home/pi/Desktop/PolyU_Attendance_System/Font.ttf'
font = ImageFont.truetype(font_file,14)

serial = spi(port=0,device=0)
device = ssd1309(serial)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((10, 40), "is found! Re-sending...", font = font,fill="white")
sleep(10000)

print("done")

#Reference
#https://github.com/rm-hull/luma.examples
#https://luma-oled.readthedocs.io/en/latest/python-usage.html
#https://luma-core.readthedocs.io/en/latest/interface.html#luma.core.interface.serial.spi
#https://luma-oled.readthedocs.io/en/latest/hardware.html
