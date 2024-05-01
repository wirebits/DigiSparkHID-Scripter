# DigiSparkHID Scripter
# A GUI tool which generates the digispark hid code by typing mnemonics.
# Author - WireBits

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

KEY_keys = {
    'A': 'KEY_A', 'B': 'KEY_B', 'C': 'KEY_C', 'D': 'KEY_D', 'E': 'KEY_E', 'F': 'KEY_F', 'G': 'KEY_G',
    'H': 'KEY_H', 'I': 'KEY_I', 'J': 'KEY_J','K': 'KEY_K', 'L': 'KEY_L', 'M': 'KEY_M', 'N': 'KEY_N',
    'O': 'KEY_O', 'P': 'KEY_P', 'Q': 'KEY_Q', 'R': 'KEY_R', 'S': 'KEY_S', 'T': 'KEY_T', 'U': 'KEY_U',
    'V': 'KEY_V', 'W': 'KEY_W', 'X': 'KEY_X', 'Y': 'KEY_Y', 'Z': 'KEY_Z', '0':'KEY_0', '1':'KEY_1',
    '2':'KEY_2', '3':'KEY_3', '4':'KEY_4', '5':'KEY_5', '6':'KEY_6', '7':'KEY_7', '8':'KEY_8',
    '9':'KEY_9', 'F1': 'KEY_F1', 'F2': 'KEY_F2', 'F3': 'KEY_F3', 'F4': 'KEY_F4', 'F5': 'KEY_F5',
    'F6': 'KEY_F6', 'F7': 'KEY_F7', 'F8': 'KEY_F8', 'F9': 'KEY_F9', 'F10': 'KEY_F10', 'F11': 'KEY_F11',
    'F12': 'KEY_F12', 'ENTER': 'KEY_ENTER'
}

MOD_keys = {'CTRL': 'MOD_CONTROL_LEFT', 'SHIFT': 'MOD_SHIFT_LEFT', 'ALT': 'MOD_ALT_LEFT', 'GUI':'MOD_GUI_LEFT'}

ASCII_keys = {
      'BKSP': '42', 'INSERT': '73', 'DEL': '76', 'TAB': '43', 'HOME': '74', 'END': '77',
      'PGUP': '75', 'PGDN': '78', 'LEFT': '80', 'UP': '82', 'RIGHT': '79', 'DOWN': '81', 'CAPS': '57',
      'SCROLL': '71', 'NUM': '83', 'ESC': '41', 'PTRSCR': '70', 'PAUSE': '72', '`': '53', '-': '45', '=': '46', '[': '47',
      ']': '48', ';': '51', "'": '52', ',': '54', '.': '55', '/': '56', 'SPACE': '44', '\\':'49'
}

class DigisparkHIDConverter:
    @staticmethod
    def convert_to_digispark_script(digispark_mnemonic):
        if digispark_mnemonic.startswith("TYPE"):
            string_text = digispark_mnemonic.split(" ", 1)[1]
            if "\\" in string_text and '\\"' not in string_text:
                string_text = string_text.replace("\\", r"\\")
            string_text = string_text.replace('"', r'\"')
            return f" DigiKeyboard.print(\"{string_text}\");"
        elif digispark_mnemonic.startswith("TYNL"):
            string_text = digispark_mnemonic.split(" ", 1)[1]
            if "\\" in string_text and '\\"' not in string_text:
                string_text = string_text.replace("\\", r"\\")
            string_text = string_text.replace('"', r'\"')
            return f" DigiKeyboard.println(\"{string_text}\");"
        elif digispark_mnemonic.startswith("PRESS"):
            keys = digispark_mnemonic.split()[1:]
            press_code = ""
            if len(keys) == 1:
                key = keys[0]
                key_code = KEY_keys.get(key, MOD_keys.get(key, ASCII_keys.get(key)))
                press_code = f" DigiKeyboard.sendKeyStroke({key_code});"
            if len(keys) == 2:
                key1 = keys[1]
                key2 = keys[0]
                key1_code = KEY_keys.get(key1, MOD_keys.get(key1, ASCII_keys.get(key1)))
                key2_code = KEY_keys.get(key2, MOD_keys.get(key2, ASCII_keys.get(key2)))
                press_code = f" DigiKeyboard.sendKeyStroke({key1_code},{key2_code});"
            if len(keys) == 3:
                key1 = keys[0]
                key2 = keys[1]
                key3 = keys[2]
                key1_code = KEY_keys.get(key1, MOD_keys.get(key1, ASCII_keys.get(key1)))
                key2_code = KEY_keys.get(key2, MOD_keys.get(key2, ASCII_keys.get(key2)))
                key3_code = KEY_keys.get(key3, MOD_keys.get(key3, ASCII_keys.get(key3)))
                press_code = f" DigiKeyboard.sendKeyStroke({key3_code},{key1_code}|{key2_code});"
            return press_code
        elif digispark_mnemonic.startswith("WAIT"):
            delay_time = int(digispark_mnemonic.split(" ")[1])
            return f" DigiKeyboard.delay({delay_time});"
        else:
            return digispark_mnemonic

class DigisparkHIDMain:
    def __init__(self, main_window):
        self.main_window = main_window
        self.create_widgets()

    def create_widgets(self):
        self.main_window.title("DigiSparkHID Scripter")
        self.main_window.resizable(0, 0)

        main_split_frame = ttk.Frame(self.main_window)
        main_split_frame.pack(side="top", fill="both", expand=True)

        self.mnemonic_frame = tk.Text(main_split_frame, font='courier 10', fg='black')
        self.mnemonic_frame.pack(side="left", fill="both", expand=True)
        self.mnemonic_frame.insert(tk.END, "Enter your mnemonic")

        self.arduino_frame = tk.Text(main_split_frame, font='courier 10', fg='black')
        self.arduino_frame.pack(side="right", fill="both", expand=True)
        self.arduino_frame.insert(tk.END, "Your digispark script")

        self.mnemonic_frame.bind("<FocusIn>", self.clear_placeholder)
        self.mnemonic_frame.bind("<Button-1>", self.disable_convert_button)

        buttons_frame = ttk.Frame(self.main_window)
        buttons_frame.pack(side="top", fill="x")

        self.convert_button = ttk.Button(buttons_frame, text="Convert", command=self.convert_text, state=tk.DISABLED)
        self.convert_button.pack(side="left", padx=5, pady=5)

        copy_button = ttk.Button(buttons_frame, text="Copy", command=self.copy_text)
        copy_button.pack(side="left", padx=5, pady=5)

        reset_button = ttk.Button(buttons_frame, text="Reset", command=self.reset_all)
        reset_button.pack(side="left", padx=5, pady=5)

        save_button = ttk.Button(buttons_frame, text="Save", command=self.save_file)
        save_button.pack(side="left", padx=5, pady=5)

        exit_button = ttk.Button(buttons_frame, text="Exit", command=self.exit_window)
        exit_button.pack(side="right", padx=5, pady=5)

    def clear_placeholder(self, event):
        if event.widget.get(1.0, tk.END).strip() == "Enter your mnemonic":
            event.widget.delete(1.0, tk.END)

    def disable_convert_button(self, event):
        self.convert_button.configure(state=tk.NORMAL)
    
    def convert_text(self):
        mnemonic_script = self.mnemonic_frame.get(1.0, tk.END).strip()
        if not mnemonic_script:
            self.arduino_frame.delete(1.0, tk.END)
            self.arduino_frame.insert(tk.END, "Enter some mnemonics to convert!")
        else:
            mnemonics = "#include<DigiKeyboard.h>\nvoid setup()\n{\n"
            for line in mnemonic_script.splitlines():
                if line.startswith("REDO"):
                    parts = line.split()
                    num_iterations = int(parts[1])
                    mnemonics += f" for (int i=1; i<={num_iterations}; i++)\n"
                    mnemonics += " {\n"
                    for mnemonic in " ".join(parts[2:]).split(","):
                        converted_line = DigisparkHIDConverter.convert_to_digispark_script(mnemonic.strip())
                        mnemonics += f" {converted_line}\n"
                        mnemonics += " }\n"
                else:
                    converted_line = DigisparkHIDConverter.convert_to_digispark_script(line.strip())
                    mnemonics += converted_line + '\n'
            mnemonics += "}\nvoid loop()\n{\n //Nothing to do here ;)\n}"
            self.arduino_frame.delete(1.0, tk.END)
            self.arduino_frame.insert(tk.END, mnemonics)
            self.arduino_frame.mark_set(tk.INSERT, "end-1c linestart")

    def copy_text(self):
        self.main_window.clipboard_clear()
        self.main_window.clipboard_append(self.arduino_frame.get(1.0, tk.END))

    def reset_all(self):
        self.mnemonic_frame.delete(1.0, tk.END)
        self.mnemonic_frame.insert(tk.END, "Enter your mnemonic")
        self.arduino_frame.delete(1.0, tk.END)
        self.arduino_frame.insert(tk.END, "Your arduino script")
        self.convert_button.configure(state=tk.DISABLED)

    def exit_window(self):
        self.main_window.destroy()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('Arduino Files', '*.ino')], defaultextension='.ino')
        if not file_path:
            return
        with open(file_path, 'w') as file:
            file.write(self.arduino_frame.get(1.0, tk.END))

main_window = tk.Tk()
app = DigisparkHIDMain(main_window)
main_window.mainloop()