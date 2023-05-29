#!/usr/bin/python3
# sudo apt-get install bluetooth bluez blueman
# pip3 install pybluez

import bluetooth

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

scan_device()