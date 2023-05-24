import mqttsetup
import time
import x728battery_monitor as battery
import input_control
import urllib.request
import subprocess
import random

def wifi_check(host='http://ia.ic.polyu.edu.hk'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return 'connected'
    except:
        return 'disconnected'

def battery_check():
    v,c = battery.capture_battery_status_int()
    return v,c

def find_wifi_detail():
    ssid = ''
    inet_addr = None

    # Get ssid
    try:
        output = str(subprocess.check_output(['sudo', 'iwgetid']))
    except:
        output = ''
    if "ESSID" in output:
        index = output.find("ESSID")
        start = index + 7
        end = len(output) - 4
        ssid = output[start:end]

    #  Get ip
    if('PolyU' in ssid):
        #PolyUWLAN
        cmd = "ifconfig | grep 255.255.224.0"
        inet = subprocess.check_output(cmd, shell = True)
        inet = inet.decode('utf-8')
        inet_addr = inet[13:28] 
    if('EIA' in ssid):
        #EIA311MESH
        cmd = "ifconfig | grep 255.255.255.0"
        inet = subprocess.check_output(cmd, shell = True)
        inet = inet.decode('utf-8')
        inet_addr = inet[13:26]

    return ssid,inet_addr

# Random number to indicate alive
def still_alive():
    return random.randint(1, 100)

def status_publish():
    node = None
    print("Thread of dashboard is running ...")
    #MQTT Init
    server = 'ia.ic.polyu.edu.hk'
    # Topic: PAD02/system_status (example)
    topic = input_control.machine_id + '/system_status'
    while node is None:
        node = mqttsetup.mqtt_client_setup(server)
    print("Connected to MQTT Server:",server)
    print("Publishing to topic:",topic)
    
    while (node is not None):
        voltage,capacity = battery_check()
        wifi_status = wifi_check()
        ssid,ip_address = find_wifi_detail()
        alive = still_alive()
        mqtt_message = mqttsetup.mqtt_message_generator(capacity,voltage,wifi_status,input_control.machine_id,
                                                        ssid,ip_address,alive)
        mqttsetup.mqtt_publish_record(node, topic, mqtt_message)
        time.sleep(1)
    



    
