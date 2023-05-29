"""
Hardware setup for GM65 Barcode reader
1) Config as USB Virtual COM Port
2) Config as Command Triggered Mode
3) Set "Time settlement for single read" be "infinite time interval"
"""
import serial

def triggerRead(ser):
    cmd=b'\x7e\x00\x08\x01\x00\x02\x01\xab\xcd'
    ser.write(cmd)
    
print("start")
ser = serial.Serial('/dev/ttyACM0')
triggerRead(ser)
result=""

while (True):
  c=ser.read()
  if (c > b'\x1f'):
     result=result+c.decode("utf-8")
  if c==b'\r':
    if (len(result)>2):
        result=result[2:]
    print(result)
    result=""
    mode=input("quit? (y/n)")
    if  mode=="n":
       triggerRead(ser)
    else:
       break

