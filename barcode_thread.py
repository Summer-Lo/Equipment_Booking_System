#!/usr/bin/python3
#Barcode scanner
import serial
import time
import csv
#Customized libraries
import display_control as display_setup
import input_control as input_setup
import file_processing as file_handle
import keypad_control as keypad_setup

barcode_scanner = '/dev/ttyACM0'
barcode = ""

barcode_on= False # by Alex
classcode_ready = False
locationcode_ready = False

classcode = ''
location = ''

classcode_type = 'ClassCode'
locationcode_type = 'LocationCode'

csv_name = input_setup.date_now() + '-' +input_setup.time_now(2)
csv_name_complete = ''

special_file = False

id_reader = None


"""
Hardware setup for GM65 Barcode reader
1) Config as USB Virtual COM Port
2) Config as Command Triggered Mode
3) Set "Time settlement for single read" be "infinite time interval"
"""
# Activate barcode reader
def triggerRead():
    global id_reader
    cmd = b'\x7e\x00\x08\x01\x00\x02\x01\xab\xcd'
    id_reader.write(cmd)

def decode_lowercase(code,sub_code):
    i = code.find(sub_code)
    return i

def get_class_details(code,display):
    code_type = 'UNKOWN'
    output = ''
    global csv_name,csv_name_complete
    global special_file
    global classcode
    #if((len(code)==9)and(not(classcode_ready))and(code[0]=='2')):
    if((not(classcode_ready))and(code[0]=='2')):
        #It is a class code
        code_type = classcode_type
        output = code
        if(not(special_file)):
            csv_name = input_setup.date_now() + '-' +input_setup.time_now(2)
            csv_name_complete = "data/" + output + "_" + csv_name + ".csv"
            file_handle.save_csv_name(csv_name_complete)
        else:
            csv_name = file_handle.read_csv_name()

        if(locationcode_ready):
            with open(csv_name_complete,'a') as data_file:
                writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([input_setup.machine_id,classcode_type,output,input_setup.date_now(),input_setup.time_now(),0])
        else:
            with open(csv_name_complete,'w') as data_file:
                writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([input_setup.machine_id,classcode_type,output,input_setup.date_now(),input_setup.time_now(),0])

        display_setup.OLED_print_msg(display,"Classcode:",output,">Scan Loc ...")
        classcode = output
        time.sleep(1)
    if (not(classcode_ready))and((code[0]!='U')and(code[0]!='W')and(code[0]!='Y')):
        # strange code
        #It is a weird classcode
        code_type = classcode_type
        output = code
        if(not(special_file)):
            csv_name = input_setup.date_now() + '-' +input_setup.time_now(2)
            csv_name_complete = "data/" + output + "_" + csv_name + ".csv"
            file_handle.save_csv_name(csv_name_complete)
        else:
            csv_name = file_handle.read_csv_name()

        if(locationcode_ready):
            with open(csv_name_complete,'a') as data_file:
                writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([input_setup.machine_id,classcode_type,output,input_setup.date_now(),input_setup.time_now(),0])
        else:
            with open(csv_name_complete,'w') as data_file:
                writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([input_setup.machine_id,classcode_type,output,input_setup.date_now(),input_setup.time_now(),0])

        display_setup.OLED_print_msg(display,"Classcode:",output,">Scan Loc ...")
        classcode = output
        time.sleep(1)

    else:

        #It is a location code
        index = decode_lowercase(code,'xxx')
        if(index == -1):
            output = code
            print("len output:",len(output))
        else:
            #Remove xxx
            output = code[0:index]+code[(index+3):len(code)]
            print("len output:",len(output))
        #if((not(locationcode_ready))and((output[0]=='W')or(output[0]=='U')or(output[0]=='Y'))):
        if((not(locationcode_ready))):
            code_type = locationcode_type
            #If classcode cannot found
            if(not(classcode_ready)):
                csv_name_complete = 'data/other_'+ output + '-' + input_setup.date_now() + '-' +input_setup.time_now(2) +'.csv'
                file_handle.save_csv_name(csv_name_complete)
                special_file = True
                with open(csv_name_complete,'w') as data_file:
                    writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([input_setup.machine_id,locationcode_type,output,input_setup.date_now(),input_setup.time_now(),1])
            else:
                csv_name_complete = file_handle.read_csv_name()
                with open(csv_name_complete,'a') as data_file:
                    writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([input_setup.machine_id,locationcode_type,output,input_setup.date_now(),input_setup.time_now(),1])
        else:
            if((locationcode_ready)and((len(output)==4)or(len(output)==5))):
                csv_name_complete = file_handle.read_csv_name()
                with open(csv_name_complete,'a') as data_file:
                    writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([input_setup.machine_id,locationcode_type,output,input_setup.time_now(),1])

        display_setup.OLED_print_msg(display,"Location:",output,">Scan ClassID ..")
        global location
        location = output
        time.sleep(1)

    return output,code_type

def barcode_scanner_init(mode):
    global id_reader # by alex
    id_reader = serial.Serial(barcode_scanner)
    print("Trigger Mode:",mode)
#    if(mode==0):
#       # Only turn on when session status = 0
#        triggerRead()
    barcode = ''
    return id_reader,barcode

def id_filter(barcode):
    # Remove meaningless '31' from barcode reader
    while(barcode[0]=='3')and(barcode[1]=='1'):
        barcode = barcode[2:len(barcode)]

    return barcode

def capture_loop(OLED_screen,status):
    global classcode_ready,locationcode_ready,csv_name_complete
    global special_file
    global id_reader
    #Barcode Setup

#    id_reader,barcode = barcode_scanner_init(status)
    dummy,barcode = barcode_scanner_init(status) #by Alex


    #Number of triggers
    max_trigger = 1
    num_trigger = 0

    print("Thread of barcode scanner is running...")
    barcode=""
    while (True):
        c_input=id_reader.read()
        # End of input
        if c_input==b'\r':
            print("Raw input:",barcode)
            barcode = id_filter(barcode)
            print("Barcode input:",barcode)

            #Reset for another phase
            if(keypad_setup.section_end):
                print("New section!")
                classcode_ready = False
                locationcode_ready = False
                keypad_setup.section_end = False
                special_file = False
                num_trigger = 0
                triggerRead()

            #Log classcode and locations
            if not(keypad_setup.resume)or (keypad_setup.reject_info):
                # Create new section
                if(not(classcode_ready))or(not(locationcode_ready)):
                    qrcode,code_type = get_class_details(barcode,OLED_screen)
                    print("type:",code_type)
                    if(code_type == classcode_type):
                        classcode_ready = True

                    if(code_type == locationcode_type):
                        locationcode_ready = True


                    print("classcode_ready:{} locationcode_ready:{}".format(classcode_ready,locationcode_ready))
                    # Reset and trigger
                    if (classcode_ready == False) or (locationcode_ready==False):
                        time.sleep(0.5)
                        triggerRead()
                    barcode = ""
            #else:
            #    classcode_ready,locationcode_ready = True,True

            # Display summary and handle rejection
            if((classcode_ready)and(locationcode_ready)and(not(keypad_setup.confirm_start))):
				# Showing confirmation message
                global location,classcode
                a = "Room:" + location
                b = "Class:" + classcode
                c = ">[0]-BACk [D]-Ok"

                display_setup.OLED_print_msg(OLED_screen,a,b,c)

            # Re create session
            if(keypad_setup.reject_info):
                print("hi")
                location = ''
                classcode = ''
                classcode_ready = False
                locationcode_ready = False
                barcode = ""


            if((classcode_ready)and(locationcode_ready)and(keypad_setup.confirm_start)):

                if(keypad_setup.confirm_start):
                    # Start taking attendance
                    file_handle.student_id = barcode
                    if(barcode != file_handle.instructor_id)and(file_handle.student_id != ''):
                        file_handle.write_to_csv(csv_name_complete,file_handle.studentcode_type)
                        barcode_backup = barcode
                        #barcode = input_setup.maskID(barcode)
                        display_setup.OLED_print_id(OLED_screen,barcode)
                    else:
                        barcode_backup = barcode
                        file_handle.write_to_csv(csv_name_complete,file_handle.staffcode_type)
                    # Terminate session
                    print("End:",keypad_setup.section_end)
                    if(keypad_setup.section_end):
                        print("try to re trigger")
                        input_setup.instructor_release_sys(OLED_screen,barcode_backup)
                        triggerRead()
                        barcode = ''
            else:
#                triggerRead()
                barcode = ''


        # Cummulating input characters
        if (c_input > b'\x1f'):
            barcode=barcode+c_input.decode("utf-8")