import struct
import smbus
import sys
import time

def voltage_to_cap(voltage):
     capacity = 0
     capacity = int(76.9*(voltage-3))
     return capacity

def readVoltage(bus):
     address = 0x36
     read = bus.read_word_data(address, 2)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     voltage = swapped * 1.25 /1000/16
     return voltage

def readCapacity(bus):
     address = 0x36
     read = bus.read_word_data(address, 4)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     capacity = swapped/256
     return capacity

def capture_battery_status():
    bus = smbus.SMBus(1)
    voltage = readVoltage(bus)
    capacity = readCapacity(bus)

    capacity = str(voltage_to_cap(voltage))+"%"
    voltage = str(round(voltage,2)) + "V"
    print("Voltage:",voltage)
    print("Capacity:",capacity)

    return voltage,capacity

def capture_battery_status_int():
    bus = smbus.SMBus(1)
    voltage = readVoltage(bus)
    capacity = readCapacity(bus)

    capacity = int(capacity)
    voltage = round(voltage,2)


    return voltage,capacity   
