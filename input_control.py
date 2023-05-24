#ID Data Processing
import time
import datetime
import evdev
from evdev import InputDevice, categorize, ecodes
import file_processing as file_handle
import display_control as display_setup
import keypad_control as keypad_setup

#by Alex
turnon_barcode=False

#Machine parameters3
machine_id = 'PAD01'
card_reader = 'AST LTD., HongKong AST HID Reader.'

# ASCIICode Scanning
scancodes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'Tap', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'xxx', 56: u'LALT',  57: u' ', 100: u'RALT'
}

NOT_RECOGNIZED_KEY = u'X'

#Search for card reader
def hardware_search(show_info,device_name):
    target_device = 'UNKOWN'
    for device_path in evdev.list_devices():
        device = evdev.InputDevice(device_path)
        if(show_info):
            print("[INFO] Deivce Path:",device.path)
            print("[INFO] Device Name:",device.name)
            print("[INFO] Device Phys:",device.phys)
            print("\r\n")
        if(device.name == device_name):
            target_device = device.path
    return target_device

def date_now():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today = str(today)
    return today 

# System Time
def time_now(display_type=1):
    if(display_type == 1):
        now = datetime.datetime.now().strftime("%H:%M:%S")
    else:
        now = datetime.datetime.now().strftime("%H-%M-%S")
    now = str(now)
    return now

# ID Masking with **
def maskID(ID):
    end=len(ID)-2
    result=ID[0]+ID[1:end].replace(ID[1:end],"*"*(end-1)+ID[end:len(ID)])
    return result

# Initialize reader
def reader_init():
    machine_event = hardware_search(True,card_reader)
    if(machine_event != 'UNKOWN'):
        device = InputDevice(machine_event) # Replace with your device
    else:
        print("[WARNING] Card Reader does not found!")
    barcode = ''
    return device,barcode 

# Check instructor ID format
def check_instructor_id(ID,format_length=6):
    #Take L94XXX as an example
    if(len(ID)==format_length):
        print("Valid Instructor detected!")
        return True
    else:
        print("Invalid Instructor detected!")
        return False

# Release system by instructor ID
def instructor_enable_sys(display,barcode):
    global turnon_barcode
    file_handle.instructor_enable = True
    if(file_handle.instructor_enable):
        file_handle.instructor_id = barcode
        print("Instructor:",file_handle.instructor_id)  
        display_setup.OLED_print_msg(display,'Staff ID:'+file_handle.instructor_id,'>Scan Room code','>[0] to back')
# Restart the session 
def instructor_release_sys(display,barcode):
    print("Input:",barcode)
    print("instructor:",file_handle.instructor_id)
    #if(file_handle.instructor_id == barcode):
    display_setup.OLED_print_msg(display,'System Released!','Attedance System ','is READY!')  
    time.sleep(1)
    #Send file
    save_path = file_handle.read_csv_name()
    send_to_server = file_handle.send_file_sftp(save_path,display)
    if(send_to_server):
        display_setup.OLED_print_msg(display,'Attendance File ','is sent to the server')
        #Initialize file status
        file_handle.change_session_status(0)
    else:
        display_setup.OLED_print_msg(display,'Wait for ','WiFi connection')
        file_handle.change_session_status(0)
    time.sleep(2)
    #Reset everything
    file_handle.instructor_enable = False
    file_handle.instructor_id = 'x'
    file_handle.student_id = 'x'
    keypad_setup.instructor_reg = False
    keypad_setup.key_buffer = ""
    keypad_setup.manual_input_phase = 0
    keypad_setup.double_confirm = False
    keypad_setup.resume = False
    keypad_setup.user_resume_input = False
    keypad_setup.reject_info = False
    keypad_setup.confirm_start = False
    keypad_setup.first_csv_access = True
    datetime = date_now()[5:]+" "+time_now()
    display_setup.OLED_print_msg(display,datetime,">Tap staff card","to start class")
#    display_setup.OLED_print_msg(display,"Please input","your staff id","to start the system!")
    print("system release ok!")

def instructor_delete_sys():
    #Reset everything
    file_handle.instructor_enable = False
    file_handle.instructor_id = 'x'
    file_handle.student_id = 'x'
    keypad_setup.instructor_reg = False
    keypad_setup.key_buffer = ""
    keypad_setup.manual_input_phase = 0
    keypad_setup.double_confirm = False
    keypad_setup.resume = False
    keypad_setup.user_resume_input = False
    keypad_setup.reject_info = False
    keypad_setup.confirm_start = False
    keypad_setup.section_end = True
    print("system release ok!")
    #Initialize file status
    file_handle.change_session_status(0)

