


# Text Expander

This is a Python script that acts as a text expander, replacing predefined abbreviations with their corresponding expansions as you type. The script uses the `pynput` library to monitor keyboard input and automatically expands abbreviations in real-time.

## Features

- Monitors keyboard input for predefined abbreviations.
- Replaces abbreviations with their expanded forms.
- Loads abbreviations and expansions from an external file.
- Simulates natural typing of the expanded text.

## Requirements

- Python 3.x
- `pynput` library
- `pyperclip` library

## Installation

1. Clone the repository or download the script files.
2. Install the required libraries using pip:

   ```bash
   pip install pynput pyperclip
   ```

3. Create an `expansions.txt` file in the same directory as the script with the following format:

   ```
   abbreviation:expansion
   ```

   Example `expansions.txt`:

   ```
   brb:be right back
   omw:on my way
   idk:I don't know
   smh:shaking my head
   btw:by the way
   ```

## Usage

1. Save the script to a file, for example, `text_expander.py`.
2. Run the script from your terminal:

   ```bash
   python text_expander.py
   ```

3. The script will start monitoring your keyboard input. When you type an abbreviation followed by a space or enter, it will replace the abbreviation with the expanded text.

## Script Explanation

- **`load_expansions(file_path)`**: This function reads the abbreviations and expansions from the specified file and returns a dictionary.
- **`on_press(key)`**: This function is called every time a key is pressed. It appends the typed characters to a buffer and processes the text when a space or enter key is detected.
- **`process_typed_text()`**: This function processes the typed text, checks if it matches any abbreviation, and replaces it with the expanded text by simulating backspace and typing the expanded text.

## Customization

- To add or modify abbreviations and their expansions, edit the `expansions.txt` file.
- Adjust the typing speed by modifying the sleep duration in the `process_typed_text()` function.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to discuss improvements and enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This script uses the `pynput` library to monitor keyboard input and simulate key presses.
- The `pyperclip` library is used for clipboard operations.

---

**Disclaimer**: This script is provided as-is. Use it at your own risk. The author is not responsible for any potential issues caused by the usage of this script.


### Instructions for Use:

1. **Copy and Paste**: Copy the above content and save it in a file named `README.md` in the same directory as your script.
2. **Customize as Needed**: Adjust any sections to better fit your specific use case or additional features.
