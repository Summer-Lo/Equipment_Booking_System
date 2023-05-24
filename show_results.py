#!/usr/bin/python3
import csv


file_path = "/home/pi/Desktop/PolyU_Attendance_System/data/demo.csv"

with open(file_path, mode='r') as id_readings:
    rows = csv.reader(id_readings)
    for row in rows:
        if(len(row)==5):
            print(row[0],row[1],row[2],row[3],row[4])
