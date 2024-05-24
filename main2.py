import evdev
from evdev import UInput, ecodes
import time

# Create a virtual input device
ui = UInput()

# Function to simulate key presses
def type_text(text):
    for char in text:
        if char.isalpha():
            keycode = ecodes.ecodes['KEY_' + char.upper()]
        elif char == ' ':
            keycode = ecodes.KEY_SPACE
        else:
            continue  # Skip unsupported characters for simplicity
        ui.write(ecodes.EV_KEY, keycode, 1)
        ui.write(ecodes.EV_KEY, keycode, 0)
        ui.syn()
        time.sleep(0.1)  # Add delay between key presses for testing

# Simulate typing "hello world"
type_text("hello world ")

# Close the virtual input device
ui.close()