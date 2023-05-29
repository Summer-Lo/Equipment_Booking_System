#pip3 install pad4pi
from pad4pi import rpi_gpio


# Setup Keypad
KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
]

COL_PINS = [19,7,18,14] # BCM numbering
ROW_PINS = [20,16,26,21] # BCM numbering


factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

def printKey(key):
    print("Received Key:",key)

# printKey will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(printKey)

while True:
    x = 0
