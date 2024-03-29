
import evdev
from evdev import InputDevice, categorize, ecodes

id_reader = InputDevice('/dev/input/event2')
barcode = ""


# ASCIICode Scanning
scancodes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT',  57: u' ', 100: u'RALT'
}

NOT_RECOGNIZED_KEY = u'X'

while True:
    for event in id_reader.read_loop():
        if event.type == ecodes.EV_KEY:
            eventdata = categorize(event)
            if eventdata.keystate == 1: # Keydown
                scancode = eventdata.scancode
                if scancode == 28:
                    print("Device input:",barcode)
                    barcode = ''
                else:
                    # Before END OF INPUT
                    key = scancodes.get(scancode, NOT_RECOGNIZED_KEY)
                    barcode = barcode + key
                    if key == NOT_RECOGNIZED_KEY:
                        print('unknown key, scancode=' + str(scancode))

