#!/bin/bash
sudo apt install figlet toilet
figlet -c  PolyU PAD
echo "[SYS] PAD System is about to upgrade"
echo "[SYS] The system is mmaintained by Vincent Chan "
echo "[SYS] Please ensure that you have put this sciprt under /home/pi"

# Backup all csv files
echo "[SYS] Start to backup all data"
sudo cp /home/pi/Desktop/PolyU_Attendance_System/data/*.csv /home/pi/pad_data_backup/
sudo cp /home/pi/Desktop/PolyU_Attendance_System/data/send_buffer/*.csv /home/pi/pad_data_backup/send_buffer/
echo "[SYS] Backup done!"

# Remove old PAD
cd Desktop/
sudo rm -r PolyU_Attendance_System/
echo "[SYS] Previous PAD is removed successfully."

# Download new PAD
git clone https://github.com/vincent51689453/PolyU_Attendance_System.git

# Remind the developer to modify some files
echo "[SYS] The new PAD is downloaded successfully."
echo "[SYS] Now you have serveral things to edit in order to finish the upgrade process."
echo "[SYS] 1. Edit \"machine_id\" inside input_control.py to match the physical device id"
echo "[SYS] 2. Check the OLED_draw_cover in display_control.py has to correct version number with respect to the tag."

