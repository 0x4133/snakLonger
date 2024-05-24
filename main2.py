import evdev
from evdev import InputDevice, categorize, ecodes
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

typed_text = []  # Buffer to store typed characters

def log_typed_text():
    word = ''.join(typed_text).strip()
    logging.debug(f"Typed text so far: {word}")

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
            if hasattr(key_event, 'keycode'):
                keycode = key_event.keycode
                if keycode.startswith('KEY_'):
                    char = keycode[4:].lower()
                    if char.isalpha():
                        typed_text.append(char)
                        logging.debug(f"Typed character: {char}")
                    elif keycode == 'KEY_SPACE':
                        typed_text.append(' ')
                        log_typed_text()
                    elif keycode == 'KEY_ENTER':
                        log_typed_text()
                        typed_text.clear()
        elif key_event.keystate == key_event.key_up:
            logging.debug(f"Key released: {key_event.keycode}")