import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
VK_BACK = 0x08

# Windows API functions and data structures
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", ctypes.c_ulong),
        ("scanCode", ctypes.c_ulong),
        ("flags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


def low_level_keyboard_handler(nCode, wParam, lParam):
    if nCode == 0 and wParam == WM_KEYDOWN:
        kb_data = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        vk_code = kb_data.vkCode
        char = chr(vk_code).lower()

        if char.isprintable():
            typed_text.append(char)
            logging.debug(f"Typed character: {char}")
        elif vk_code == VK_BACK:
            if typed_text:
                typed_text.pop()
        elif vk_code == 0x20:  # Space key
            typed_text.append(" ")
            process_typed_text()
            typed_text.clear()

    return user32.CallNextHookEx(hook_id, nCode, wParam, lParam)


def set_hook():
    hook_proc = ctypes.WINFUNCTYPE(
        ctypes.c_long, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
    )(low_level_keyboard_handler)
    return user32.SetWindowsHookExA(
        WH_KEYBOARD_LL, hook_proc, kernel32.GetModuleHandleW(None), 0
    )


def simulate_typing(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.01)


def process_typed_text():
    try:
        word = "".join(typed_text).strip()
        logging.debug(f"Typed word: {word}")

        if word in expansions:
            expanded_text = expansions[word]
            logging.debug(f"Expanding: {word} -> {expanded_text}")

            backspace_count = len(word) + 1
            for _ in range(backspace_count):
                print("\b \b", end="", flush=True)
                time.sleep(0.01)

            simulate_typing(expanded_text + " ")

    except Exception as e:
        logging.error(f"Error processing typed text: {e}")


def load_expansions(file_path):
    expansions = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                if ":" in line:
                    abbreviation, expansion = line.strip().split(":", 1)
                    expansions[abbreviation.strip()] = expansion.strip()
        logging.info(f"Loaded expansions: {expansions}")
    except Exception as e:
        logging.error(f"Error loading expansions: {e}")
    return expansions


def main():
    global hook_id, typed_text, expansions
    expansions = load_expansions("expansions.txt")
    typed_text = []

    hook_id = set_hook()

    try:
        logging.info("Text expander started.")
        msg = ctypes.wintypes.MSG()
        while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageA(ctypes.byref(msg))
    except KeyboardInterrupt:
        logging.info("Text expander stopped.")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        user32.UnhookWindowsHookEx(hook_id)


if __name__ == "__main__":
    main()
