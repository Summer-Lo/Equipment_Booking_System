import evdev


for device_path in evdev.list_devices():
    device = evdev.InputDevice(device_path)
    print("Deivce Path:",device.path)
    print("Device Name:",device.name)
    print("Device Phys:",device.phys)
    print("\r\n")
