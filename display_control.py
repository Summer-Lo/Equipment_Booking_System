#OLED Configurations
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1309
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#List out SPI channels
#ls -l /dev/spi*
#spidev<port>.<device>

# Display parameters
SCREEN_LINES = 4
SCREEN_SAVER = 20.0
CHAR_WIDTH = 19
font = ImageFont.load_default()
width = 128
height = 64
FONT_SIZE = 14
FONT_PATH = '/home/pi/Desktop/PolyU_Attendance_System/Font.ttf'

# Initialize 128x64 display with hardware SPI
def OLED_setup():
    serial = spi(port=0,device=0)
    device = ssd1309(serial)
    return device


# Draw welcome cover on OLED
def OLED_draw_cover(disp):  
    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype(FONT_PATH, 12)
    font10 = ImageFont.truetype(FONT_PATH,10)
    with canvas(disp) as draw:
        draw.rectangle(disp.bounding_box, outline="white", fill="black")
        draw.text((10, 10), "Portable", font = font,fill="white")
        draw.text((10, 25), "Attendance", font = font,fill="white")
        draw.text((10, 40), "Device v3.1", font = font,fill="white") 


# Print barcode result on LED
def OLED_print_id(disp,ID):
    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype(FONT_PATH, 12)
    font10 = ImageFont.truetype(FONT_PATH,13)
    with canvas(disp) as draw:
        draw.text((0,0), 'Date: {}'.format(time.strftime("%Y/%m/%d")), font = font,fill="white")
        draw.text((0,20), 'Time: {}'.format(time.strftime("%H:%M:%S")), font = font, fill = "white")    
        draw.text((0,40), 'ID: {}'.format(ID), font = font, fill = "white")        
        print("[INFO] Masked ID:",ID)

# Print customized message on LED
def OLED_print_msg(disp,line1_msg=' ',line2_msg=' ',line3_msg=' '):
    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype(FONT_PATH, 14)
    font10 = ImageFont.truetype(FONT_PATH,13)

    with canvas(disp) as draw:
        draw.text((0,0), line1_msg, font = font, fill = "white")
        draw.text((0,20), line2_msg, font = font, fill = "white")    
        draw.text((0,40), line3_msg, font = font, fill = "white")        

