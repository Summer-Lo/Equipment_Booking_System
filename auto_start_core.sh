echo "If you want to disable auto_start_core.sh, please follow the instructions below"

echo "Remove Exec = lxterminal --command=\"/home/pi/auto_start.sh\" in /home/pi/.config/autostart/LXinput-setup.desktop"

cd /home/pi/Desktop/PolyU_Attendance_System
#lxterminal -e "sudo /home/pi/sugar-wifi-conf/build/sugar-wifi-conf pisugar /home/pi/sugar-wifi-conf/build/custom_config.json"
lxterminal -e "python3 core.py" 
#lxterminal -e "python ./test_code/x728_battery.py"
