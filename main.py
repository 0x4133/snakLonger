import logging
from pynput import keyboard
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def load_expansions(file_path):
    """
    Load expansions from a file.
    Each line in the file should be in the format: abbreviation:expansion
    """
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


# Load expansions from the file
expansions = load_expansions('expansions.txt')

typed_text = []  # Buffer to store typed characters
controller = keyboard.Controller()  # Initialize the controller


def on_press(key):
    try:
        if hasattr(key, 'char') and key.char:
            typed_text.append(key.char)
            logging.debug(f"Typed character: {key.char}")
        elif key in {keyboard.Key.space, keyboard.Key.enter}:
            typed_text.append(' ')
            process_typed_text()
            typed_text.clear()
    except Exception as e:
        logging.error(f"Error on key press: {e}")


def process_typed_text():
    try:
        word = ''.join(typed_text).strip()
        logging.debug(f"Typed word: {word}")

        if word in expansions:
            expanded_text = expansions[word]
            logging.debug(f"Expanding: {word} -> {expanded_text}")

            # Simulate pressing backspace to delete the abbreviation and space
            backspace_count = len(word) + 1
            for _ in range(backspace_count):
                controller.press(keyboard.Key.backspace)
                controller.release(keyboard.Key.backspace)
                logging.debug("Pressed backspace")
                time.sleep(0.01)

            # Simulate typing the expanded text
            for char in expanded_text + ' ':
                controller.type(char)
                logging.debug(f"Typed character: {char}")
                
    except Exception as e:
        logging.error(f"Error processing typed text: {e}")


# Set up the keyboard listener
try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    logging.info("Text expander stopped.")
except Exception as e:
    logging.error(f"Error starting listener: {e}")