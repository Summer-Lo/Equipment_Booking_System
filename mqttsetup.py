import paho.mqtt.client as mqtt


def mqtt_client_setup(server):
    client = mqtt.Client()
    client.connect(server,1883,60)
    return client


def mqtt_publish_record(node,topic,mqtt_message):
    node.publish(topic, mqtt_message)
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