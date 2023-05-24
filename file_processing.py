#File processing 
import pysftp
import csv
import input_control as input_setup
import bluetooth
import display_control as display_setup
import time
import os

#sftp server info
sHostName = '158.132.153.195'		
sUserName = 'pad'
sPassWord = '42004200'			
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
#cnopts.hostkeys.load('~/.ssh/known_hosts')
local_path = "/home/pi/Desktop/PolyU_Attendance_System/data/send_buffer/" 
remote_path = "/home/pad/data/"


#Data variables
instructor_enable = False
instructor_id = 'x'
student_id = 'x'

studentcode_type = "StudentCode"
staffcode_type = "StaffCode"

public_csv_name = ''

def rename_csv():
    print("Start renaming csv ...")
    target_name = ''
    classcode = ''
    locationcode = ''

    target_name = read_csv_name()
    try:
        #Search for locationcode and classcode
        with open(target_name, mode='r') as id_readings:
            rows = csv.reader((line.replace('\0','') for line in id_readings))
            for row in rows:
                if(row[1] == 'ClassCode'):
                    classcode = row[2]
                if(row[1] == 'LocationCode'):
                    locationcode = row[2]
        new_name = classcode + '-' +locationcode + '-' +input_setup.date_now() + '-' +input_setup.time_now(2) + '.csv'
        cmd = 'sudo cp ' + target_name + ' ' + 'data/send_buffer/' + new_name 
        print("System cmd:",cmd)
        os.system(cmd)
        #save_csv_name(new_name)
    except:
        #If using old file
        new_name = target_name
    return new_name
  
# Write record to csv
def write_to_csv(file_name,code_type=studentcode_type):
    global instructor_id,student_id
    index = 0
    #Find Previous Record Serial No.
    with open(file_name, mode='r') as id_readings:
        rows = csv.reader((line.replace('\0','') for line in id_readings))
        for row in rows:
            try:
                if('PAD' in row[0]):
                    index += 1  
            except:
                x = 0

    # the a is for append, if w for write is used then it overwrites the file
    f = open(file_name, mode='a',encoding='utf-8')
    with f as id_readings:
        id_write = csv.writer(id_readings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if(code_type == studentcode_type):
            id_write.writerow([input_setup.machine_id,studentcode_type,student_id,input_setup.date_now(),input_setup.time_now(),index])

        if(code_type == staffcode_type):
            id_write.writerow([input_setup.machine_id,staffcode_type,instructor_id,input_setup.date_now(),input_setup.time_now(),index])        
        # Force write to hard drive
        f.flush()
        # Make sure data written to hard drive are effective
        os.fsync(f.fileno())

    student_id = 'x'

    # Just display the content of the csv
    with open(file_name, mode='r') as id_readings:
        rows = csv.reader((line.replace('\0','') for line in id_readings))
        for row in rows:
            print(row)


# Send file through sftp
def send_file_sftp(csv_name,display):
    global local_path,remote_path 
    send_ok = False

    try:
        #Accept any host key 
        with pysftp.Connection(host=sHostName,username=sUserName,password=sPassWord,private_key=".ppk",cnopts=cnopts) as sftp:
            # srv.cwd('/root/public'): #Write the whole path
            #upload file to server
            file_to_send = rename_csv()
            local_path_complete = local_path + file_to_send
            remote_path_complete = remote_path + file_to_send
            print("Local File Path:",local_path_complete)
            print("Remote File Path:",remote_path_complete)
            sftp.put(local_path_complete, remote_path_complete) 
            local_path_complete = local_path
            remote_path_complete = remote_path
        change_session_status(0)
        send_ok = True
    except:
        #When wifi is not avaliable
        display_setup.OLED_print_msg(display,'Wifi is not','avaliable. File','is not sent!')
        change_session_status(1)
        time.sleep(2)
    return send_ok
        

# Scan bluetooth devices
def scan_device():
    print("Scanning devices...")
    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)
    num_of_devices = len(devices)
    print(num_of_devices,"devices found")
    for addr,name,device_class in devices:
        print("Device:")
        print("Device Name: %s" % (name))
        print("Device MAC Address: %s" % (addr))
        print("Device Class: %s" % (device_class))
        print("\n") 

#Read public csv file name
def read_csv_name():
    file_path = open("public_csv_name.txt","r")
    name = file_path.read()
    print("File name:",name)
    file_path.close()
    return name

#Save public csv file name
def save_csv_name(file_name):
    file_path = open("public_csv_name.txt","w")
    file_path.write(file_name)
    print("File name saved!")
    file_path.close()

# Count unique students in a csv
def count_student_id():
    buffer_list = []
    num_student = 0

    target_file = read_csv_name()
    # Save ALL students ID first
    with open(target_file, mode='r') as id_readings:
        rows = csv.reader((line.replace('\0','') for line in id_readings))
        for row in rows:
            if('StudentCode' in row):
                #Recombine csv items to string
                x = ''
                for i in range(0,len(row)):
                    x += row[i] + ','
                #print('x=',x)
                id_start = x.find('StudentCode') + len('StudentCode') + 1
                id_end = id_start
                end_of_id = False
                while not end_of_id:
                    if(x[id_end] == ','):
                        end_of_id = True
                    id_end += 1
                buffer_list.append(x[id_start:id_end-1])

            """
            if(row[1] == 'StudentCode'):   
                buffer_list.append(row[2])
            """
        
    unqiue_list = []
    for x in buffer_list:
        if x not in unqiue_list:
            unqiue_list.append(x)
            num_student += 1
    
    return num_student


# Change session status
def change_session_status(status):
    file_path = 'session_status.csv'
    if (status == 0):
        # Session is closed and uploaded to the server
        f = open(file_path, mode='w')
        with f as status_log:
            file_status = csv.writer(status_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_status.writerow([0,input_setup.date_now(),input_setup.time_now()])
            os.fsync(f)
    if (status == 1):
        # Session is closed but failed to upload because of wifi conditions
        f = open(file_path, mode='w')
        with f as status_log:
            file_status = csv.writer(status_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_status.writerow([1,input_setup.date_now(),input_setup.time_now()])  
            os.fsync(f)  
    if (status == 2):
        # Session is closed because the device is shutdown. It should contine when the system restarts
        f = open(file_path, mode='w')
        with f as status_log:
            file_status = csv.writer(status_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_status.writerow([2,input_setup.date_now(),input_setup.time_now()])
            os.fsync(f)


# Check session status in csv
def read_session_status():
    file_path = 'session_status.csv' 
    file_status = 0         
    #Search for session status in the csv
    with open(file_path, mode='r') as id_readings:
        rows = csv.reader(id_readings)
        for row in rows:
            file_status = row[0]
    
    return file_status
