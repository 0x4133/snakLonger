import evdev
from evdev import InputDevice, categorize, ecodes

# Find the input device
devices = [InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)

# Replace 'your_device_path' with the actual device path found above
device_path = '/dev/input/eventX'  # replace X with the appropriate number

device = InputDevice(device_path)

# Start listening to the input device
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        if key_event.keystate == key_event.key_down:
            print(f"Key pressed: {key_event.keycode}")
        elif key_event.keystate == key_event.key_up:
            print(f"Key released: {key_event.keycode}")