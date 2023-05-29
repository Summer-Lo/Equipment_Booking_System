import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    global connection
    if(rc == 0):
        print("Connected with result code "+str(rc))
        conenction = 1
    else:
        print("Failed to connect, return code %d\n",rc)
        connection = 0
        
def on_disconnect(client,userdata,rc):
    global connection
    print("MQTT client disconnected!")
    connection = 0

def mqtt_client_setup(server):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(server,1883,60)
    return client


def mqtt_publish_record(client,topic,mqtt_message):
    result = client.publish(topic, mqtt_message)
    status = result[0]
    if status == 0:
        print(f"Send `{mqtt_message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    #node.loop_stop()
    #node.disconnect()

def mqtt_message_generator(battery_cap,voltage,wifi_status,machine_id,ssid,ip,alive):
    #Generate message for node red dashboard display
    
    cap = '"' + machine_id + '_capacity"'
    v = '"' + machine_id + '_voltage"'
    w = '"' + machine_id + '_wifi_status"'
    ip_address = '"' + machine_id + '_IPv4"'
    network = '"' + machine_id + '_ssid"'
    alive_msg = '"' + machine_id + '_life"'

    wifi_status = '"' + wifi_status + '"'
    ssid = '"' + ssid + '"'
    ip = '"' + ip + '"'

    mqtt_message =' { '+ cap +':' + str(battery_cap)+ \
                ','+ v +':'+ str(voltage)+ \
                ','+ w +':'+wifi_status+\
                ','+ ip_address +':'+ip+\
                ','+ network +':'+ssid+\
                ','+ alive_msg +':'+str(alive)+\
                 ' } '
    print(mqtt_message)
    return mqtt_message

def mqtt_bookMessage_generator(student_id,datetime,location):
    #Generate message for node red dashboard display

    mqtt_message =' { "ID": "' + str(student_id)+ '"'\
                ',"Datetime": "' + str(datetime)+ '"'\
                ',"Location": "' + str(location)+ '"'\
                 ' } '
    #print(mqtt_message)
    return mqtt_message 
