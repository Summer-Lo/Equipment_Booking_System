import display_control as display_setup
import time
import csv

# Delay for 90s
counter = 10
i = 0
OLED_screen = display_setup.OLED_setup()

# Dummy access to session_status.csv
def dummy_read_session_csv(file_path):
	#Search for session status in the csv
	with open(file_path, mode='r') as session:
		rows = csv.reader(session)
		for row in rows:
			status = row[0]
			print("Status:",status)
	

while (i<counter):
	progress = "--> "+str(int(i/counter*100))+"%"
	display_setup.OLED_print_msg(OLED_screen,"System is starting...","Clock is sync-ing...",progress)
	dummy_read_session_csv('session_status.csv')
	time.sleep(1)
	i += 1

