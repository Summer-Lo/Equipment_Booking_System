#4x4 Membrane Keypad Configuration

#pip3 install pad4pi
from pad4pi import rpi_gpio
import display_control as display_setup
import file_processing as file_handle
import input_control as input_setup
import x728battery_monitor as battery
import urllib.request
import csv
import dashboard_control as dashboard
import time

# Setup Keypad
KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
]
# BCM numbering
# R1 R2 R3 R4  C1 C2 C3 C4
#[20,16,26,21][19,7,18,14]

COL_PINS = [19,7,18,14]
ROW_PINS = [20,16,26,21]


#Display screen
display_device = None
#Input procedures
manual_input_phase = 0
#ID storage
key_buffer = ""
#Instructor Register
instructor_reg = False
#Flag for section close
section_end = False
#Flag for double confirm
double_confirm = False
#Section resume check
resume = False
#Confirm info of session creation
confirm_start = False
#Reject all info of session creation
reject_info = False
#first access to csv
first_csv_access = True
temp_csv = None

def wifi_check(host='http://ia.ic.polyu.edu.hk'):
    """
    try:
        urllib.request.urlopen(host) #Python 3.x
        ssid, ip = dashboard.find_wifi_detail()
        return 'connected',ip
    except:
        return 'disconnected','None'
    """
    ssid,ip = dashboard.find_wifi_detail()
    if(ssid == ''):
        return 'disconnected','None'
    else:
        return 'connected',ip

def manual_input_id(key,screen):
    global manual_input_phase,key_buffer,instructor_reg
    global section_end,double_confirm
    global resume,user_resume_input
    global confirm_start,rejct_info
    #Special Key Event

    # Check number of unique student ids
    if(key == "A"):
        z = file_handle.count_student_id()
        num_student = str(z)
        if(z>=10):
            num_student_msg = "Num of students:"+num_student
            display_setup.OLED_print_msg(screen,"CSV File Analyze",num_student_msg,"")
        else:
            num_student_msg = "Num of students:"
            display_setup.OLED_print_msg(screen,"CSV File Analyze",num_student_msg,num_student)        
        time.sleep(2)
        display_setup.OLED_print_msg(screen,"Please continue","your operations","Thanks")

    #Battery check and wifit status
    if(key == "B"):
        display_setup.OLED_print_msg(screen,"Start checking","system status...","Please wait ....")
        time.sleep(1)
        print("[INFO] start checking device status")
        v,c = battery.capture_battery_status()
        wifi,ip = wifi_check()
        battery_stats = v +" "+c
        wifi_stats = "IP :" + ip
        datetime = input_setup.date_now()[5:]+" "+input_setup.time_now()
        display_setup.OLED_print_msg(screen,battery_stats,datetime,wifi_stats)
        time.sleep(2)
        display_setup.OLED_print_msg(screen,"Please continue","your operations","Thanks")

    #Confirming input session correct  
    if(key == "D"):
        confirm_start = True
        display_setup.OLED_print_msg(screen,"Session Start!",">Tap student card","to register")

    if(key == "0"):
        if not confirm_start:
            # You can reject all the information before session creation
            reject_info = True
            display_setup.OLED_print_msg(screen,"Info rejected!","Please start again",".......")
            time.sleep(1)
            datetime = input_setup.date_now()[5:]+" "+input_setup.time_now()
            display_setup.OLED_print_msg(screen,datetime,">Tap staff card","to start class")
            file_handle.instructor_id = 'x'
            file_handle.student_id = 'x'
            input_setup.instructor_delete_sys()
    
    
    #Instructor release system
    if(key == "C"):
        # Double confirm mechanism
        if not(double_confirm):
            wifi,ip = wifi_check()
            if(wifi == 'disconnected'):
                display_setup.OLED_print_msg(screen,"wifi is not ready","please do it later","")
                file_handle.change_session_status(1)
                double_confirm = False
            else:
                # Double confirm only works when wifi is ready
                display_setup.OLED_print_msg(screen,"wifi is ready!","Press <C> if you ","are sure.")
                #display_setup.OLED_print_msg(screen,"wifi is not ready","please do it later","")
                double_confirm = True
        else:
            datetime = input_setup.date_now()[5:]+" "+input_setup.time_now()
            display_setup.OLED_print_msg(screen,datetime,">Tap staff card","to end class")
            instructor_reg = False
            section_end = True
        

    if(key == "*"):
        if(manual_input_phase == 0):
            #Manual input phase 0 -> OLED display instructions
            display_setup.OLED_print_msg(screen,"Please type ID :","<*> to confirm ","<#> to re-enter")
            manual_input_phase = 1

        elif(manual_input_phase == 1):
            #User Finish input -> ready to send
            manual_input_phase = 0
            display_setup.OLED_print_msg(screen,"ID:"+key_buffer,"OK! ","")
            if(not(file_handle.instructor_enable)):
                # Always ask for instructor ID
                input_setup.instructor_enable_sys(screen,key_buffer)
            else:
                if(section_end):
                    # Terminate session
                    input_setup.instructor_release_sys(screen,key_buffer)

                # Studen manual input for attendance record
                file_handle.student_id = key_buffer
                save_path = file_handle.read_csv_name()
                file_handle.write_to_csv(save_path,file_handle.studentcode_type)

            key_buffer = ""

        else:
            #Nothing here yet
            p = 0

    #Manual input phase 1 -> Remove input
    if(key == "#"):
        if(manual_input_phase == 1):
            key_buffer = ""
            display_setup.OLED_print_msg(screen,key_buffer,">[*] to confirm ",">[#] to re-enter")

    #Manual input phase 1 -> Input ID
    if(manual_input_phase == 1):
        if(key!="*")and(key!="#"):
            #Does not record special key characters
            key_buffer += str(key)
            display_setup.OLED_print_msg(screen,key_buffer,">[*] to confirm ",">[#] to re-enter")

    #Section resume [YES]
    if((key == '1')and(not user_resume_input)):
        resume = True
        user_resume_input = True
    
    #Section resume [NO]
    if((key == '2')and(not user_resume_input)):
        resume = False
        user_resume_input = True



def keypad_init(display):
    global display_device
    display_device = display
    factory = rpi_gpio.KeypadFactory()
    keypad_4X4 = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    return keypad_4X4

def keypad_capture(key):
    global display_device
    print("[INFO] Input {} detected!".format(key))
    manual_input_id(key,display_device)

