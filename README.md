# PolyU_Attendance_System
It is an E-attendance Taking System of Timetabled Class. It is reponsible for electronic timekepping and recording of all PolyU students attending IC timetabled classes starting from AY2021/2022.

**System Operattion Guidelines**
----------------------------
### Situation 1: Previous file was uploaded to server sucessfully
1. Power ON and wait until the cover screen appear
2. The screen will display "no incomplete session found!"
3. Tap your staff id card
3. Scan classcode by barcode scanner (QRcode)
4. Scan location by barcode scanner (QRcode)
5. Press \<D\> to confirm all information. Press \<0\> to start over.
6. Input students ID to record the attendance (Press * to use keypad)
8. Close the system by pressing \<C\> in the keypad and input staff id
9. Press \<B\> to check battery status
10. Press \<A\> to get the number of unqiue student id instantly
11. Power OFF the device by pressing the button for 7-8 seconds.

### Situation 2: Previous file was not completed but device was shutdown (power saving)
1. Power ON and wait until the cover screen appear
2. The screen will display "incomplete session found! Re-starting..."
3. The screen will display "Please tap your ID card below"
4. Input students ID to record the attendance (Press * to use keypad)
5. Close the system by pressing \<C\> in the keypad and input staff id
6. Press \<B\> to check battery status
7. Press \<A\> to get the number of unqiue student id instantly
8. Power OFF the device by pressing the button for 7-8 seconds.

### Situation 3: Previous file was completed but cannot be uploaded to server (network does not exist)
1. Power ON and wait until the cover screen appear
2. The screen will display "complete session found! Re-sending..."
3. The screen will display "Please tap your ID card below"
4. Just wait until you see "Attendance File is sent to the server"
5. Power OFF the device by pressing the button for 7-8 seconds.

**Hardware setup for GM65 Barcode reader**
----------------------------
1. Config as USB Virtual COM Port
2. Config as Command Triggered Mode
3. Set "Time settlement for single read" be "infinite time interval"

**Data Record Fomat**
----------------------------
The csv file will be saved as such format: \<classcode\>-\<room\>-\<date and time\>.csv
| Device      | Type         | Data        | Date & Time          | Index |
| ----------- | ------------ | ----------- |--------------------- | ------|
| PAD02       | LocationCode | W402A       | 2021-05-12,10:46:34  | 0     |
| PAD02       | ClassCode    | 20D030T01   | 2021-05-12,10:46:35  | 1     |
| PAD02       | StaffCode    | L12354      | 2021-05-12,10:46:36  | 2     |
| PAD02       | StudentCode  | 12345678A   | 2021-05-12,10:46:37  | 3     |

**Dashboard Support**
----------------------------
All the implemened PAD nodes are publishing system status to MQTT server. Battery capacity associated with voltage level and wifi status are shown in the node red server.
![image](https://github.com/vincent51689453/PolyU_Attendance_System/blob/main/git_image/dashboard.JPG)

**Software Support**
----------------------------
1. Put the upgrade/system_upgrade.sh to /home/pi and execute
2. Edit "machine_id" inside input_control.py to match the physical device id
3. Edit session_status.csv and confirm the first integer is 0.
4. Check the OLED_draw_cover in display_control.py has to correct version number with respect to the tag.
5. If you need to access WPA2 Enterprise network, please use upgrade/wpa2_support.sh.

**Product Layout**
----------------------------
![image](https://github.com/vincent51689453/PolyU_Attendance_System/blob/main/git_image/card_reader01.jpg)

![image](https://github.com/vincent51689453/PolyU_Attendance_System/blob/main/git_image/card_reader02.jpg)

![image](https://github.com/vincent51689453/PolyU_Attendance_System/blob/main/git_image/card_reader03.jpg)

![image](https://github.com/vincent51689453/PolyU_Attendance_System/blob/main/git_image/card_reader04.jpg)

