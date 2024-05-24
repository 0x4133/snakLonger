import evdev
from evdev import InputDevice, categorize, ecodes
import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def load_expansions(file_path):
    expansions = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if ':' in line:
                    abbreviation, expansion = line.strip().split(':', 1)
                    expansions[abbreviation.strip()] = expansion.strip()
        logging.info(f"Loaded expansions: {expansions}")
    except Exception as e:
        logging.error(f"Error loading expansions: {e}")
    return expansions

expansions = load_expansions('expansions.txt')

typed_text = []  # Buffer to store typed characters

def process_typed_text():
    try:
        word = ''.join(typed_text).strip()
        logging.debug(f"Typed word: {word}")

        if word in expansions:
            expanded_text = expansions[word]
            logging.debug(f"Expanding: {word} -> {expanded_text}")

            # Simulate pressing backspace to delete the abbreviation and space
            for _ in range(len(word) + 1):
                print("BACKSPACE")  # Placeholder for actual backspace simulation
                time.sleep(0.01)

            # Simulate typing the expanded text
            for char in expanded_text + ' ':
                print(char, end='', flush=True)  # Placeholder for actual typing simulation
                logging.debug(f"Typed character: {char}")
                time.sleep(0.01)

    except Exception as e:
        logging.error(f"Error processing typed text: {e}")

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
                        process_typed_text()
                        typed_text.clear()
                    elif keycode == 'KEY_ENTER':
                        process_typed_text()
                        typed_text.clear()
        elif key_event.keystate == key_event.key_up:
            logging.debug(f"Key released: {key_event.keycode}")