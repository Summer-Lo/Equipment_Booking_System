#!/usr/bin/python
import SH1106
import RPi.GPIO as GPIO
import time
import datetime
import evdev
import csv
import config
import traceback
import pysftp
import sys
import subprocess
import os
import string
import pysftp

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


from evdev import InputDevice, categorize, ecodes

#GPIO define
RST_PIN  = 25 #Reset
CS_PIN   = 8
DC_PIN   = 24
#JS_P_PIN = 13 #Joystick Pressed
BTN1_PIN = 21
BTN2_PIN = 20
BTN3_PIN = 16

#sftp server info
sHostName = 'ia.ic.polyu.edu.hk'		
sUserName = 'pad'
sPassWord = '42004200'			
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
#cnopts.hostkeys.load('~/.ssh/known_hosts')
local_path = "/home/pad/demo.csv"
remote_path = "demo.csv"


# Some constants
SCREEN_LINES = 4
SCREEN_SAVER = 20.0
CHAR_WIDTH = 19
font = ImageFont.load_default()
width = 128
height = 64
x0 = 0
x1 = 84
y0 = -2
y1 = 12
x2 = x1+7
x3 = x1+14
x4 = x1+9
x5 = x2+9
x6 = x3+9
FONT_SIZE = 14

# init GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(BTN1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
state = 0 #System state: 0 - scrren is off; equal to channel number (e.g. BTN2_PIN, JS_P_PIN) otherwise



# 240x240 display with hardware SPI:
disp = SH1106.SH1106()
disp.Init()

# Clear display.
disp.clear()


#scancodes = {
# Scancode: ASCIICode
#    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
#    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
#    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
#    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
#    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
#    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
#}

#capscodes = {
#    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
#    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
#    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
#    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
#    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
#    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT',  57: u' ', 100: u'RALT'
#}


scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT',  57: u' ', 100: u'RALT'
}



NOT_RECOGNIZED_KEY = u'X'

device = InputDevice('/dev/input/event4') # Replace with your device

barcode = ''

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (disp.width, disp.height), "RED")
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

def init():
    global image
    global draw
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (disp.width, disp.height), "RED")
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    #Font
    button_size = (20,22,36,36) #x=16,y=14
    font_type = "/home/pi/Desktop/Button/Font.ttf"
    font_size = 20
    font = ImageFont.truetype(font_type,font_size,encoding='utf-8')
    #font = ImageFont.load_default()


def date_now():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today = str(today)
    return(today)

def time_now():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    now = str(now)
    return(now)
    		
def write_to_csv():
    # the a is for append, if w for write is used then it overwrites the file
    with open('/home/pad/demo.csv', mode='a') as id_readings:
        id_write = csv.writer(id_readings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	write_to_log = id_write.writerow([date_now(),time_now(),barcode])
        showID = maskID(barcode)
        oled_print(showID)
        return(write_to_log)
	
def maskID(ID):
    end=len(ID)-2
    result=ID[0]+ID[1:end].replace(ID[1:end],"*"*(end-1)+ID[end:len(ID)])
    return result

def oled_print(ID):
    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('Font.ttf', 14)
    font10 = ImageFont.truetype('Font.ttf',13)
    #print ("***draw text")
    ID = ID.decode("utf-8")
    draw.text((0,0), 'Date: {}'.format(time.strftime("%Y/%m/%d")), font = font, fill = 0)
    draw.text((0,FONT_SIZE+5), 'Time: {}'.format(time.strftime("%H:%M:%S")), font = font, fill = 0)    
    draw.text((0,2*FONT_SIZE+10), 'ID: {}'.format(ID), font = font, fill = 0)        
    # image1=image1.rotate(180) 
    disp.ShowImage(disp.getbuffer(image1))

def title_print():
    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('Font.ttf', 16)
    font10 = ImageFont.truetype('Font.ttf',13)
    
#    print ("***draw line")
    draw.line([(0,0),(127,0)], fill = 0)
    draw.line([(0,0),(0,63)], fill = 0)
    draw.line([(0,63),(127,63)], fill = 0)
    draw.line([(127,0),(127,63)], fill = 0)
#    print ("***draw rectangle")
    
#    print ("***draw text")
    draw.text((30,0), 'Portable ', font = font, fill = 0)
    draw.text((18,20), 'Attendance', font = font, fill = 0)    
    draw.text((35,40), 'Device', font = font, fill = 0)        
#    # image1=image1.rotate(180) 
    disp.ShowImage(disp.getbuffer(image1))

def click_b1(channel):
    send_file()
    print("file sent")


def send_file():
    #Accept any host key 
    with pysftp.Connection(host=sHostName,username=sUserName,password=sPassWord,private_key=".ppk",cnopts=cnopts) as sftp:
    #  srv.cwd('/root/public'): #Write the whole path
        sftp.put(local_path, remote_path) #upload file to server l
GPIO.add_event_detect(BTN1_PIN, GPIO.RISING, callback=click_b1, bouncetime=200)
    
init()

while 1:
    title_print()
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
	    eventdata = categorize(event)
	    if eventdata.keystate == 1: # Keydown
		scancode = eventdata.scancode
		if scancode == 28: # Enter
		    write_to_csv()
		    barcode = ''
		else:
		    key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
		    barcode = barcode + key
		    if key == NOT_RECOGNIZED_KEY:
			print('unknown key, scancode=' + str(scancode))
