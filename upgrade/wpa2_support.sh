#!/bin/bash
sudo apt install figlet toilet
figlet -c WPA2 Network Support
echo "[SYS] Start to install advanced network manager"
echo "[SYS] The system is maintained by Vincent Chan "
sudo apt install network-manager network-manager-gnome

# Remove previous wpa_supplicant.conf
sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
echo "[SYS] Previous wpa config file is removed successfully."

# Copy the wpa_supplicant.conf from upgrade/ (deprecated 18 Aug 2021)
#sudo cp /home/Desktop/PolyU_Attendance_System/upgrade/wpa_supplicant.conf /etc/wpa_supplicant/
#echo "[SYSM New wpa config file is relocated successfully."

# Remind the developer to connect to the network manually for once.
echo "[SYS] The network manager is installed successfully."
echo "[SYS] Please reboot the system and connect to the network manually once."

