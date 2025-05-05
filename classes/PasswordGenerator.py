"""
Password Generator (tab)
A simple password generator with options for including different sets of characters.
"""

from classes.Utilities import *
import string

class PasswordGenerator(TabFrame):
    _name = "Password Generator"
    _description = "Generate secure passwords."
    _icon = "password generator icon.png"

    def init(self) -> None:
        self.tabname = "Password Generator"
        self.description = """A simple password generator with options for including different sets of characters."""
        self.create_widgets()
    
    def create_widgets(self) -> None:
        self.header = ttk.Label(self, text="Password Generator", font=PConstants.arial_14)
        self.header.pack(side="top", anchor="w", padx=5, pady=2)
        self.length_frame = ttk.Frame(self, height=1)
        self.length_frame.pack(side="top", anchor="nw", fill="x", padx=5, pady=2)

        self.length_label = ttk.Label(self.length_frame, text="Length:")
        self.length_label.pack(side="left", anchor="nw", padx=5, pady=2)
        self.length_entry = ttk.Entry(self.length_frame, width=35)
        self.length_entry.pack(side="left", anchor="nw", padx=5, pady=2)

        self.include_uppercase = tk.BooleanVar(self, True)
        self.include_uppercase_selector = ttk.Checkbutton(self, variable=self.include_uppercase, text="Include uppercase")
        self.include_uppercase_selector.pack(side="top", anchor="nw", padx=5, pady=2)

        self.include_numbers = tk.BooleanVar(self, True)
        self.include_numbers_selector = ttk.Checkbutton(self, variable=self.include_numbers, text="Include numbers")
        self.include_numbers_selector.pack(side="top", anchor="nw", padx=5, pady=2)

        self.include_brackets = tk.BooleanVar(self, True)
        self.include_brackets_selector = ttk.Checkbutton(self, variable=self.include_brackets, text="Include brackets")
        self.include_brackets_selector.pack(side="top", anchor="nw", padx=5, pady=2)

        self.include_special_characters = tk.BooleanVar(self, False)
        self.include_special_characters_selector = ttk.Checkbutton(self, variable=self.include_special_characters, text="Include special characters")
        self.include_special_characters_selector.pack(side="top", anchor="nw", padx=5, pady=2)

        self.result_box = ttk.Entry(self, width=40)
        self.result_box.pack(side="top", anchor="nw", padx=5, pady=2)

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(side="top", anchor="nw", expand=1, fill="x", padx=5, pady=2)
        self.generate_button = ttk.Button(self.buttons_frame, text="Generate!", command=self.generate)
        self.generate_button.pack(side="left", anchor="nw", padx=5, pady=2)
        self.copy_button = ttk.Button(self.buttons_frame, text="Copy to clipboard", command=self.copy)
        self.copy_button.pack(side="left", anchor="nw", padx=5, pady=2)
    
    def createTabCommands(self) -> None:
        self.addTabFunction("Clear", lambda: self.result_box.delete(0, tk.END))
    
    def generate(self) -> None:
        length = toInt(self.length_entry.get())
        if not length: return
        validchars = string.ascii_lowercase
        if self.include_uppercase.get(): validchars += string.ascii_uppercase
        if self.include_numbers.get(): validchars += string.digits
        if self.include_brackets.get(): validchars += "()[]{}<>"
        if self.include_special_characters.get(): validchars += "`~!@#$%^&*-_=+\\|;:'\",./?"
        self.result_box.delete(0, tk.END)
        result = ""
        for i in range(length):
            result += random.choice(validchars)
        self.result_box.insert(tk.END, result)

    def copy(self) -> None:
        if not self.result_box.get(): return
        self.clipboard_append(self.result_box.get())    