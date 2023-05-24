#!/usr/bin/python3
from evdev import InputDevice, categorize, ecodes
import time
import threading
import os
import csv
#Customized libraries
import display_control as display_setup
import input_control as input_setup
import file_processing as file_handle
import keypad_control as keypad_setup
import barcode_thread
#import dashboard_control

#Time synchronization cover
os.system('python3 /home/pi/Desktop/PolyU_Attendance_System/time_syn_cover.py')

#OLED Setup
OLED_screen = display_setup.OLED_setup()
display_setup.OLED_draw_cover(OLED_screen)
time.sleep(2)

#Reader Setup
id_reader,barcode = input_setup.reader_init()

#Keypad Setup (Interrupt)
keypad_4X4 = keypad_setup.keypad_init(OLED_screen)
keypad_4X4.registerKeyPressHandler(keypad_setup.keypad_capture)

# Check session status
os.system('sudo chmod 777 session_status.csv')
# Multiple access to obtain most update csv content
dummy = 10

readID = 0

while True:

    for event in id_reader.read_loop():
        if event.type == ecodes.EV_KEY:
            eventData = categorize(event)
            print(event)
            #display_setup.OLED_print_msg(OLED_screen,str(event))
            readID = 1
        else:
            if(readID ==0):
                datetime = input_setup.date_now()[5:]+" "+input_setup.time_now()
                display_setup.OLED_print_msg(OLED_screen,datetime,">Tap student card","to register")

