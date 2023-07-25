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
import config as host
import mqttsetup
import sys

readID = 0
datetime = input_setup.date_now()[5:]+" "+input_setup.time_now()
barcode_display = ''

def display_update(OLED_screen):
    global readID,datetime,barcode_display
    time.sleep(15)
    while True:
        if(readID == 0):
            datetime = input_setup.date_now()[5:]+" "+input_setup.time_now()
            display_setup.OLED_print_msg(OLED_screen,datetime,">Tap student card","to register "+host.location)
            #print(datetime)
            time.sleep(1)
        elif(readID == 2):
            datetime = input_setup.date_now()[5:]+" "+input_setup.time_now()
            display_setup.OLED_print_id(OLED_screen,barcode_display)
            barcode_display = ''
            time.sleep(3)
            readID = 0
        else:
            time.sleep(0.1)
            pass

# ASCIICode Scanning
scancodes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT',  57: u' ', 100: u'RALT'
}

NOT_RECOGNIZED_KEY = u'X'
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

#MQTT server Setup
client = mqttsetup.mqtt_client_setup(host.server)
client.loop_start()
#sclient.on_connect = on_connect

# Check session status
os.system('sudo chmod 777 session_status.csv')
# Multiple access to obtain most update csv content
dummy = 10

datetime = input_setup.date_now()[5:]+" "+input_setup.time_now()
display_setup.OLED_print_msg(OLED_screen,datetime,">Tap student card","to register "+str(host.location))

time_update = threading.Thread(target=display_update,args=(OLED_screen,))
time_update.start()

try:
    while True:
        for event in id_reader.read_loop():
            if event.type == ecodes.EV_KEY:
                eventdata = categorize(event)
                if eventdata.keystate == 1: # Keydown
                    scancode = eventdata.scancode
                    print(scancode)
                    #print("scancode:",scancode)
                    if scancode == 28:
                        print("Data:",barcode)
                        barcode_display = barcode
                        readID = 2
                        datetimeMQTT = input_setup.date_now()+" "+input_setup.time_now()+".00+0800"
                        message = mqttsetup.mqtt_bookMessage_generator(str(barcode),str(datetimeMQTT),str(host.location))
                        mqttsetup.mqtt_publish_record(client,host.topic,message)
                        print(message)
                        barcode = ''
                        scancode = ''
                        time.sleep(0.1)
                    else:
                        # Before END OF INPUT
                        datetime = input_setup.date_now()[5:]+" "+input_setup.time_now()
                        display_setup.OLED_print_msg(OLED_screen,datetime,">Loading")
                        print("scancode:",scancode)
                        key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
                        if (key!='X'):
                            barcode = barcode + key
                            print("key:",key)
                            readID = 1
            '''
            else:
                if(readID == 0):
                    datetime = input_setup.date_now()[5:]+" "+input_setup.time_now()
                    display_setup.OLED_print_msg(OLED_screen,datetime,">Tap student card","to register "+str(host.location))
                    print("NOW: ",datetime)
                    time.sleep(1)
            #elif (readID == 2):
                    
            #display_setup.OLED_print_msg(OLED_screen,datetime,">Session booked")
            '''
except KeyboardInterrupt:
    time_update.join()
    sys.exit(0)
